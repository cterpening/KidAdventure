#!/usr/bin/env python3
"""Browser gameplay smoke checks for KidAdventure.

This script uses Playwright against a temporary local static server so we can
exercise real keyboard-driven gameplay instead of relying only on static checks.
"""

from __future__ import annotations

from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


REPO_ROOT = Path(__file__).resolve().parents[1]


def snapshot(page) -> dict:
    return page.evaluate("window.__kidAdventureTest.getSnapshot()")


def wait_for(predicate, timeout: float = 5.0, interval: float = 0.05) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return
        time.sleep(interval)
    raise AssertionError("Timed out waiting for condition.")


def hold_key(page, key: str, duration_ms: int) -> None:
    page.keyboard.down(key)
    page.wait_for_timeout(duration_ms)
    page.keyboard.up(key)


def place_player_on_item(page, kind: str) -> None:
    snap = snapshot(page)
    items = {item["kind"]: item for item in snap["room"]["items"]}
    if kind not in items:
        raise AssertionError(f"Could not find item '{kind}' in room '{snap['currentRoomId']}'.")
    item = items[kind]
    target_x = item["x"] - max(0, (snap["player"]["w"] - item["w"]) / 2)
    target_y = item["y"] - max(0, (snap["player"]["h"] - item["h"]) / 2)
    page.evaluate(
        "(pos) => window.__kidAdventureTest.setPlayerPosition(pos.x, pos.y)",
        {"x": target_x, "y": target_y},
    )


@contextmanager
def local_server():
    handler = partial(SimpleHTTPRequestHandler, directory=str(REPO_ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        thread.join(timeout=2)


def run_smoke() -> None:
    with local_server() as base_url, sync_playwright() as playwright:
        browser = None
        try:
            try:
                browser = playwright.chromium.launch(channel="msedge", headless=True)
            except Exception:
                browser = playwright.chromium.launch(headless=True)

            page = browser.new_page(viewport={"width": 1400, "height": 1000})
            page.goto(f"{base_url}/index.html?level=adventure&seed=smoke", wait_until="domcontentloaded")
            page.wait_for_function("window.__kidAdventureTest && window.__kidAdventureTest.getSnapshot")
            page.locator("#game").click()
            page.wait_for_timeout(250)

            snap = snapshot(page)
            assert snap["activeLevelId"] == "adventure", snap
            assert snap["currentLayoutId"] == "classic", snap
            assert snap["currentRoomId"] == "meadow", snap

            start_x = snap["player"]["x"]
            hold_key(page, "ArrowRight", 200)
            wait_for(lambda: snapshot(page)["player"]["x"] > start_x + 10)

            page.evaluate("window.__kidAdventureTest.reset()")
            page.locator("#game").click()
            place_player_on_item(page, "sword")
            page.keyboard.press("e")
            wait_for(lambda: snapshot(page)["player"]["holding"] == "sword")

            page.keyboard.press("q")
            wait_for(lambda: snapshot(page)["player"]["holding"] is None)

            page.select_option("#levelSelect", "remix")
            wait_for(lambda: snapshot(page)["activeLevelId"] == "remix")
            remix = snapshot(page)
            assert remix["currentLayoutId"] in {"shuffled", "labyrinth", "catacombs", "highlands", "gauntlet"}, remix
            assert remix["room"] is not None, remix

            page.evaluate(
                """
                () => {
                  const snap = window.__kidAdventureTest.getSnapshot();
                  const targets = Object.values(snap.room.neighbors).filter(Boolean);
                  if (!targets.length) {
                    return null;
                  }
                  return window.__kidAdventureTest.transitionToRoom(targets[0]);
                }
                """
            )
            wait_for(
                lambda: snapshot(page)["currentRoomId"] != remix["currentRoomId"],
                timeout=3.0,
            )
        except PlaywrightTimeoutError as exc:
            raise AssertionError(f"Browser test timed out: {exc}") from exc
        finally:
            if browser is not None:
                browser.close()


def main() -> int:
    run_smoke()
    print("PASS: Browser gameplay smoke test completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
