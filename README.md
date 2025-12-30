# KidAdventure

Kid Adventure is a browser-based tribute to the Atari 2600 classic. Pick a kid-specific hero, explore maze-like overworlds, defeat dragons with the sword, unlock castles with the key, and haul the trophy back to the starting pedestal.

## How to Play
- Move with WASD/arrow keys or the on-screen D-pad (tablets/phones).
- Press `E` / "Use" to pick up items; gates open automatically when you touch them while holding the key.
- `Q` / "Drop" button drops the item you are carrying.
- Find the sword near the starting meadow, then defeat the dragon guarding the trophy.
- Carry the key up to a castle gate to swing it open, then dive deeper to grab the trophy and bring it home.

## Custom Kid Art
- Drop PNGs or JPGs into `assets/kids/<kidId>/` named `player.png`.
- Shared art (dragon, dragon-dead, key, sword, trophy) lives under `assets/common/`.
- Register new kids or swap art by editing `ASSET_CONFIG` in `index.html`.

## Deployment
1. Commit the static files (no build step required) to your repo.
2. Enable GitHub Pages for the `main` branch/root to host `index.html`.
3. Open `https://<you>.github.io/<repo>/` to play on desktop or mobile.

## Changelog
- **2025-11-19** – Added multi-kid selector, custom art manifest, and virtual touch controls.
- **2025-11-19** – Implemented multi-room layouts, dragon AI, castle silhouettes, and random layout rotation.
- **2025-11-19** – Introduced Level 1/2/3 selector with sprawling Catacombs, Highlands, and Dragon Gauntlet maps, plus HUD/layout toasts.
