# KidAdventure

KidAdventure is a family-photo remake of Atari 2600 Adventure. The goal is a recognizable Adventure-style quest first: carry one item at a time, dodge dragons, unlock castles with keys, survive the bat, and bring the trophy back to the pedestal. The project adds polish through better room landmarks, family-specific player art, and an optional remix mode instead of rewriting the core game loop.

## Game Modes
- `Adventure Mode` is the default experience. It keeps one stable overworld so players can learn routes, remember item locations, and build the same kind of map memory that makes the original game feel satisfying.
- `Remix Mode` keeps the same rules and items, but rotates through larger, more bespoke maps for variety once the classic-feeling run is familiar.

## How to Play
- Move with `WASD`, arrow keys, or the touch D-pad.
- Press `E` or `Use / Pick` to grab an item.
- Press `Q` or `Drop` to set the held item down.
- Carry the `sword` to defeat dragons.
- Carry the `bridge` to move through walls.
- Match the yellow, black, and green keys to their castle gates. The white key opens any gate.
- Survive the bat, which steals loose items and can carry them into other rooms.
- Return the `trophy` to the start pedestal to win.

## Custom Kid Art
- Put each kid's portrait/sprite at `assets/kids/<kidId>/player.png`.
- Shared item/enemy art lives in `assets/common/`.
- Register kids and asset paths in `js/content-config.js`.
- You can start directly on a kid with `?kid=<kidId>`.

## Project Direction
- Keep the base rule set close to Adventure.
- Put originality into room flavor, castle silhouettes, family art, and cleaner item presentation.
- Prefer one strong default world over constant randomization.
- Keep remix content optional so the main game still feels teachable and consistent.

## Development
- This is a static project. There is no build step.
- Open `index.html` directly in a browser, or serve the folder with a tiny static server if you prefer.
- Useful query params:
- `?kid=<kidId>`
- `?level=adventure|remix`
- `?seed=<value>`

## Quality Checks
- Run `python tools/qa_checks.py` for lightweight repository and documentation checks.
- Run `python tools/layout_checks.py` to validate room graph and secret-door connectivity.
- Run `python tools/gameplay_regressions.py` to validate item, dragon, gate, pedestal, and seeded-randomness invariants.
- Run `python tools/gameplay_browser_smoke.py` for a browser-driven smoke test that exercises live movement, pickup/drop flow, mode switching, and room loading.

## Persistence
- Save data is stored in `localStorage` under `kidAdventure.save.v1`.
- The save includes selected kid, selected mode, seed, win counters, accessibility options, debug mode, and key bindings.
- Older `l1` / `l2` / `l3` save values are migrated into the newer `adventure` / `remix` mode model at runtime.

## Accessibility
- High contrast mode is available in the sidebar.
- Colorblind gate symbols can be enabled from the sidebar.
- Item icons now also use shape cues so the keys stay readable even when colors are similar.

## Code Layout
- `index.html` contains the page structure, styles, and UI shell.
- `js/constants.js` contains canvas constants.
- `js/content-config.js` contains kid, mode, and item configuration.
- `js/game.js` contains the runtime, entity logic, rendering, rooms, and UI integration.
- `tools/` contains dependency-free validation scripts for docs, layouts, and gameplay invariants.
