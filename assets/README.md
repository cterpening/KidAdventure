# Kid asset folders

Place per-kid art inside `assets/kids/<kidId>/` so the canvas prototype can load them automatically. Each folder should contain:

- `player.png`
- `dragon.png`
- `dragon-dead.png`
- `key.png`
- `sword.png`
- `trophy.png`

Update `ASSET_CONFIG` in `index.html` to register each kid id (and optional display name) with paths to their art. At runtime you can switch kids with the `?kid=<kidId>` query string (e.g., `index.html?kid=alex`).
