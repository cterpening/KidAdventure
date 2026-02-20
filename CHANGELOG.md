# Changelog

## 2026-02-20
- Added `tools/qa_checks.py` for dependency-free lint/smoke checks and documented it in README.
- Added `tools/layout_checks.py` for static map connectivity/invariant validation across all layout builders.
- Added a non-reciprocal-neighbor allowlist to `tools/layout_checks.py` so intentional one-way paths do not hide new warnings.
- Fixed a broken Gauntlet room neighbor reference (`fortGate.south -> cliffPass`) by removing the invalid exit.
- Prevented bat-stolen items from being dropped into walls or closed gates by selecting the nearest safe drop position.
- Updated world-state checks to re-read the active room after player transitions, fixing stale-room combat/win edge cases.
- Added blur/visibility input reset so keyboard/touch state cannot stick after tab or window focus changes.
- Corrected asset documentation to match shared common sprites with optional per-kid overrides.

## 2025-11-21
- Added colored keys (yellow/black/green) plus a white master key and updated gates to match.
- Added bridge item that lets you pass through walls while carrying it.
- Added a bat that steals items and moves them between rooms.
- Added secret doors, extra rooms per layout, and larger Level 1/2/3 maps.
- Added multiple dragon types per layout with varied speed/aggro.

## 2025-11-20
- Fixed castle gates so they unlock when the key is touching them, preventing the closed gate from blocking the unlock.
- Clarified instructions that gates pop open automatically when you walk into them with the key.

## 2025-11-19
- Added kid selector and per-kid assets (Eli/Isla/Kylie) with shared dragon/key/sword/trophy art.
- Implemented touch controls (D-pad + action buttons) alongside keyboard input.
- Built multi-level map system with random variants (Classic, Shuffled, Labyrinth, Catacombs, Highlands, Gauntlet) and level selector.
- Added castle silhouettes, improved wall rendering, and refined gates/doors for castle entry.
- Placed keys near gates per layout and added item drop safety near closed gates.
- Improved responsive layout for portrait devices (canvas on top, controls below).
- Misc: dragon-dead sprite support, HUD layout tags, README instructions.
