#!/usr/bin/env python3
"""Gameplay regression checks for map/item/combat invariants."""

from __future__ import annotations

from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
GAME_JS = REPO_ROOT / "js" / "game.js"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_matching(source: str, start: int, open_ch: str, close_ch: str) -> int:
    if start >= len(source) or source[start] != open_ch:
        raise ValueError(f"Expected '{open_ch}' at index {start}.")
    depth = 0
    quote: str | None = None
    in_line_comment = False
    in_block_comment = False
    escaped = False

    i = start
    while i < len(source):
        ch = source[i]
        nxt = source[i + 1] if i + 1 < len(source) else ""

        if in_line_comment:
            if ch == "\n":
                in_line_comment = False
            i += 1
            continue
        if in_block_comment:
            if ch == "*" and nxt == "/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            i += 1
            continue

        if ch == "/" and nxt == "/":
            in_line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            in_block_comment = True
            i += 2
            continue
        if ch in ("'", '"', "`"):
            quote = ch
            i += 1
            continue

        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError(f"Unmatched '{open_ch}' at index {start}.")


def extract_function_body(source: str, function_name: str) -> str:
    marker = f"function {function_name}(world)"
    idx = source.find(marker)
    if idx < 0:
        raise ValueError(f"Could not find function '{function_name}'.")
    open_brace = source.find("{", idx)
    close_brace = find_matching(source, open_brace, "{", "}")
    return source[open_brace + 1 : close_brace]


def parse_builders(source: str) -> list[str]:
    builders = re.findall(r"builder:\s*(build[A-Za-z0-9_]+)", source)
    seen: set[str] = set()
    ordered: list[str] = []
    for builder in builders:
        if builder in seen:
            continue
        seen.add(builder)
        ordered.append(builder)
    return ordered


def main() -> int:
    text = read_text(GAME_JS)
    errors: list[str] = []
    warnings: list[str] = []

    if "Math.random(" in text:
        errors.append("Found Math.random usage; expected seeded RNG only.")
    if 'searchParams.get("seed")' not in text:
        errors.append("Missing seed query-parameter handling.")

    builders = parse_builders(text)
    if not builders:
        errors.append("No layout builders detected in LAYOUT_VARIANTS.")

    for builder in builders:
        try:
            body = extract_function_body(text, builder)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        items = re.findall(r'world\.addItemToRoom\(new Item\("([^"]+)"', body)
        item_set = set(items)
        required_keys = re.findall(r'requiredKey\s*:\s*"([^"]+)"', body)
        dragon_count = len(re.findall(r"new Dragon\(", body))
        has_pedestal = "room.pedestal" in body

        if "sword" not in item_set:
            errors.append(f"{builder}: Missing sword item placement.")
        if "trophy" not in item_set:
            errors.append(f"{builder}: Missing trophy item placement.")
        if dragon_count < 1:
            errors.append(f"{builder}: Expected at least one dragon.")
        if not has_pedestal:
            errors.append(f"{builder}: Missing pedestal setup.")

        for gate_key in required_keys:
            if gate_key == "key-white":
                continue
            if gate_key not in item_set and "key-white" not in item_set:
                errors.append(
                    f"{builder}: Gate requires '{gate_key}' but layout does not place that key (or key-white)."
                )

        if len(items) < 4:
            warnings.append(f"{builder}: Low item count ({len(items)}); verify layout difficulty intent.")

    if errors:
        print("FAIL: Gameplay regressions detected:")
        for issue in errors:
            print(f"- {issue}")
        if warnings:
            print("\nWARNINGS:")
            for issue in warnings:
                print(f"- {issue}")
        return 1

    print("PASS: Gameplay regression checks completed successfully.")
    if warnings:
        print("WARNINGS:")
        for issue in warnings:
            print(f"- {issue}")
    else:
        print("No warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
