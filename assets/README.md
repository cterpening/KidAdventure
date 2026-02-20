# Kid asset folders

Place per-kid art inside `assets/kids/<kidId>/` so the canvas prototype can load them automatically.

- Required per kid:
  - `player.png`
- Shared defaults (used by all kids unless you override paths in `ASSET_CONFIG`):
  - `assets/common/dragon.png`
  - `assets/common/dragon-dead.png`
  - `assets/common/key.png`
  - `assets/common/sword.png`
  - `assets/common/trophy.png`
  - `assets/common/bat.svg`

Update `ASSET_CONFIG` in `index.html` to register each kid id (and optional display name) with paths to their art. At runtime you can switch kids with the `?kid=<kidId>` query string (e.g., `index.html?kid=alex`).
