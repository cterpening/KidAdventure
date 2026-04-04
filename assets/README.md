# Asset Notes

KidAdventure uses shared world-item art plus per-kid player art.

## Kid Folders
- Put each player's art in `assets/kids/<kidId>/player.png`.
- Keep transparent backgrounds when possible.
- Match the existing proportions so collision and pickup visuals still read well at game scale.

## Shared Art
- `assets/common/dragon.png`
- `assets/common/dragon-dead.png`
- `assets/common/key.png`
- `assets/common/sword.png`
- `assets/common/trophy.png`
- `assets/common/bat.svg`

## Registering New Kids
- Add the kid entry to `ASSET_CONFIG` in `js/content-config.js`.
- Point the `player` path at the new `assets/kids/<kidId>/player.png`.
- If a kid needs custom shared art overrides, update that same config entry with kid-specific paths.

## Runtime Notes
- The game scales art to the active entity size at runtime.
- Keys, bridge, sword, and trophy now have extra shape-driven presentation in code so they read clearly even when the source image is minimal.
