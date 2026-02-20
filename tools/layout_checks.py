#!/usr/bin/env python3
"""Static layout/connectivity checks for KidAdventure map definitions."""

from __future__ import annotations

from collections import deque
from pathlib import Path
import re
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = REPO_ROOT / "index.html"
OPPOSITE_DIR = {"north": "south", "south": "north", "east": "west", "west": "east"}
# Intentional one-way links/gate-adjacent flows that should not fail warning scans.
ALLOWED_NON_RECIPROCAL: set[tuple[str, str, str, str]] = {
    ("buildClassicLayout", "yellowHall", "west", "yellowCourtyard"),
    ("buildShuffledLayout", "yellowHall", "west", "yellowCourtyard"),
    ("buildShuffledLayout", "riverbank", "south", "swamp"),
    ("buildShuffledLayout", "swamp", "west", "riverbank"),
    ("buildCatacombsLayout", "yellowHall", "west", "yellowCourtyard"),
    ("buildCatacombsLayout", "dragonDen", "east", "greenEntrance"),
    ("buildCatacombsLayout", "obsidianPass", "south", "blackHall"),
    ("buildHighlandsLayout", "yellowHall", "west", "yellowCourtyard"),
    ("buildHighlandsLayout", "bogDepths", "east", "blackEntrance"),
    ("buildGauntletLayout", "dragonAerie", "east", "towerHall"),
}


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


def split_top_level_args(arg_text: str) -> list[str]:
    args: list[str] = []
    start = 0
    paren = brace = bracket = 0
    quote: str | None = None
    in_line_comment = False
    in_block_comment = False
    escaped = False

    i = 0
    while i < len(arg_text):
        ch = arg_text[i]
        nxt = arg_text[i + 1] if i + 1 < len(arg_text) else ""

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

        if ch == "(":
            paren += 1
        elif ch == ")":
            paren -= 1
        elif ch == "{":
            brace += 1
        elif ch == "}":
            brace -= 1
        elif ch == "[":
            bracket += 1
        elif ch == "]":
            bracket -= 1
        elif ch == "," and paren == 0 and brace == 0 and bracket == 0:
            args.append(arg_text[start:i].strip())
            start = i + 1
        i += 1

    tail = arg_text[start:].strip()
    if tail:
        args.append(tail)
    return args


def parse_js_string(token: str) -> str | None:
    token = token.strip()
    match = re.fullmatch(r'"([^"\\]*(?:\\.[^"\\]*)*)"', token)
    if match:
        return bytes(match.group(1), "utf-8").decode("unicode_escape")
    match = re.fullmatch(r"'([^'\\]*(?:\\.[^'\\]*)*)'", token)
    if match:
        return bytes(match.group(1), "utf-8").decode("unicode_escape")
    return None


def extract_function_body(source: str, function_name: str) -> str:
    marker = f"function {function_name}(world)"
    idx = source.find(marker)
    if idx < 0:
        raise ValueError(f"Could not find function '{function_name}'.")
    open_brace = source.find("{", idx)
    close_brace = find_matching(source, open_brace, "{", "}")
    return source[open_brace + 1 : close_brace]


def parse_neighbors(options_text: str) -> dict[str, str]:
    idx = options_text.find("neighbors")
    if idx < 0:
        return {}
    open_brace = options_text.find("{", idx)
    if open_brace < 0:
        return {}
    close_brace = find_matching(options_text, open_brace, "{", "}")
    body = options_text[open_brace + 1 : close_brace]
    out: dict[str, str] = {}
    for direction, target in re.findall(r"\b(north|south|east|west)\s*:\s*\"([^\"]+)\"", body):
        out[direction] = target
    return out


def parse_rooms(
    layout_body: str,
) -> tuple[dict[str, dict[str, str]], dict[str, set[str]], list[str]]:
    rooms: dict[str, dict[str, str]] = {}
    gate_edges: dict[str, set[str]] = {}
    errors: list[str] = []
    pos = 0
    while True:
        idx = layout_body.find("addRoom(", pos)
        if idx < 0:
            break
        open_paren = idx + len("addRoom")
        close_paren = find_matching(layout_body, open_paren, "(", ")")
        args_text = layout_body[open_paren + 1 : close_paren]
        args = split_top_level_args(args_text)
        if len(args) < 3:
            errors.append("Encountered addRoom call with too few arguments.")
            pos = close_paren + 1
            continue

        room_id = parse_js_string(args[0])
        if not room_id:
            errors.append(f"Could not parse room id from addRoom arg: {args[0][:40]}")
            pos = close_paren + 1
            continue

        if room_id in rooms:
            errors.append(f"Duplicate room id '{room_id}'.")
        neighbors = parse_neighbors(args[2])
        rooms[room_id] = neighbors
        gate_edges.setdefault(room_id, set())
        if len(args) >= 4:
            for target in re.findall(r'targetRoom\s*:\s*"([^"]+)"', args[3]):
                gate_edges[room_id].add(target)
        pos = close_paren + 1

    return rooms, gate_edges, errors


def parse_secret_doors(layout_body: str) -> list[tuple[str, str]]:
    doors: list[tuple[str, str]] = []
    pos = 0
    while True:
        idx = layout_body.find("addSecretDoor(", pos)
        if idx < 0:
            break
        open_paren = idx + len("addSecretDoor")
        close_paren = find_matching(layout_body, open_paren, "(", ")")
        args = split_top_level_args(layout_body[open_paren + 1 : close_paren])
        if len(args) >= 3:
            source_match = re.search(r"\bworld\.rooms\.([A-Za-z0-9_]+)\b", args[0].strip())
            source_room = source_match.group(1) if source_match else None
            target_room = parse_js_string(args[2])
            if source_room and target_room:
                doors.append((source_room, target_room))
        pos = close_paren + 1
    return doors


def reachable_rooms(graph: dict[str, set[str]], start_room: str) -> set[str]:
    seen: set[str] = set()
    queue = deque([start_room])
    while queue:
        room = queue.popleft()
        if room in seen:
            continue
        seen.add(room)
        for next_room in graph.get(room, set()):
            if next_room not in seen:
                queue.append(next_room)
    return seen


def main() -> int:
    text = read_text(INDEX_HTML)
    errors: list[str] = []
    warnings: list[str] = []

    start_match = re.search(r'const\s+START_ROOM_ID\s*=\s*"([^"]+)";', text)
    if not start_match:
        print("FAIL: Could not parse START_ROOM_ID from index.html.")
        return 1
    start_room = start_match.group(1)

    builders = re.findall(r"builder:\s*(build[A-Za-z0-9_]+)", text)
    if not builders:
        print("FAIL: No layout builders found in LAYOUT_VARIANTS.")
        return 1

    seen_builders: set[str] = set()
    ordered_builders: list[str] = []
    for b in builders:
        if b not in seen_builders:
            seen_builders.add(b)
            ordered_builders.append(b)

    for builder in ordered_builders:
        try:
            body = extract_function_body(text, builder)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        rooms, gate_edges, parse_errors = parse_rooms(body)
        for e in parse_errors:
            errors.append(f"{builder}: {e}")
        if not rooms:
            errors.append(f"{builder}: No rooms parsed.")
            continue

        if start_room not in rooms:
            errors.append(f"{builder}: Missing START_ROOM_ID room '{start_room}'.")

        for room_id, neighbors in rooms.items():
            for direction, target in neighbors.items():
                if target not in rooms:
                    errors.append(
                        f"{builder}: Room '{room_id}' has {direction} neighbor '{target}' that does not exist."
                    )
                    continue
                opposite = OPPOSITE_DIR[direction]
                target_back = rooms[target].get(opposite)
                if target_back != room_id:
                    if (builder, room_id, direction, target) in ALLOWED_NON_RECIPROCAL:
                        continue
                    warnings.append(
                        f"{builder}: Non-reciprocal neighbor {room_id}.{direction} -> {target} "
                        f"(expected {target}.{opposite} -> {room_id}, found {target_back!r})."
                    )

        transitions: dict[str, set[str]] = {room_id: set() for room_id in rooms}
        for room_id, neighbors in rooms.items():
            transitions[room_id].update(neighbors.values())

        for room_id, targets in gate_edges.items():
            for target in targets:
                if target not in rooms:
                    errors.append(f"{builder}: Gate target '{target}' from '{room_id}' does not exist.")
                    continue
                transitions[room_id].add(target)

        for source_room, target_room in parse_secret_doors(body):
            if source_room not in rooms:
                errors.append(
                    f"{builder}: Secret door source '{source_room}' does not exist in this layout."
                )
                continue
            if target_room not in rooms:
                errors.append(
                    f"{builder}: Secret door target '{target_room}' does not exist in this layout."
                )
                continue
            transitions[source_room].add(target_room)

        if start_room in rooms:
            seen = reachable_rooms(transitions, start_room)
            unreachable = sorted(r for r in rooms if r not in seen)
            if unreachable:
                errors.append(
                    f"{builder}: Unreachable room(s) from '{start_room}': {', '.join(unreachable)}."
                )

    if errors:
        print("FAIL: Layout checks found issues:")
        for issue in errors:
            print(f"- {issue}")
        if warnings:
            print("\nWARNINGS:")
            for issue in warnings:
                print(f"- {issue}")
        return 1

    print("PASS: Layout checks completed successfully.")
    if warnings:
        print("WARNINGS:")
        for issue in warnings:
            print(f"- {issue}")
    else:
        print("No warnings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
