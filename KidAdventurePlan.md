# KidAdventure Multi-Profile Adventure (Web)

## Vision
- Web-friendly reimagining of the Atari 2600 Adventure game loop (explore rooms, pick up objects, defeat a dragon) with modern kid-specific artwork.
- Landing page acts as a "choose your hero" hub: every kid gets their own profile tile, color palette, and adventure variant.
- Each kid page is a single-screen app that loads their assets (avatar, castle, dragon) and story beats while reusing shared game logic.

## Feature Breakdown
1. **Landing Page**
   - Grid of cards, each displaying a kid's photo/drawing, nickname, difficulty indicator.
   - Settings button to toggle accessibility mode (high contrast, dyslexia-friendly font).
   - Simple local JSON (`kids.json`) controls which profiles appear, making it easy to add/remove kids without code changes.
2. **Kid Adventure Page**
   - Loads by hash/route (e.g., `/index.html#alex`) or via simple router (React/Preact optional but not required).
   - Phaser, Kaboom, or lightweight canvas engine handles sprite movement, collision, inventory.
   - All textual narration pulled from kid-specific data so stories remain personal.
3. **Shared Systems**
   - Asset loader that swaps spritesheets/background music based on profile id.
   - Save data stored via `localStorage` per kid (progress stars, collected items).
   - Photo upload utility (optional) to let adults update avatars safely offline.

## Hosting on GitHub
1. Create (or reuse) a public repo named `kid-adventure`.
2. Place the landing page at `/index.html`, kid routes share that file.
3. Enable GitHub Pages (Settings → Pages → `main` branch → `/root`).
4. Push updates; GH Pages auto-builds static assets—no backend needed.
5. For custom domain, configure DNS (CNAME) but not required.

## Tablet-First Considerations
- 16:9 responsive layout with safe zones so touch overlays never hide game HUD.
- Virtual joystick + two action buttons sized 52–60 px with generous spacing.
- Preload textures/audio to avoid lag on mobile Safari; fall back to static images if WebGL unavailable.
- Add `Add to Home Screen` instructions for iOS/Android to mimic an app.
- Offline-ready via basic Service Worker (cache landing page, JSON, sprites).

## Suggested Stack
- Base: Vanilla Vite (or Parcel) bundling plain JS modules for fast reloads.
- Game Engine: Phaser 3 (solid collision + input) or Kaboom.js for simpler API.
- Styling: CSS variables per kid, plus Tailwind or Sass if desired.
- Data: `/data/kids/alex.json` etc. describing palette, hero sprite, story text.
- Media: Store kid-specific art in `/public/assets/kids/<name>/`.

## Content Workflow
1. Define kids in `kids.json` (id, displayName, color, heroSprite, storyBlurb).
2. Export kid art at consistent resolution (e.g., 64 px tiles) to keep physics tuning constant.
3. Use template script to scaffold new kid data folder + default sprites.
4. Adults can drop photos into `assets/raw/` and run a script to generate optimized PNG/WebP.

## Development Roadmap
1. Prototype the landing page + profile selection UI.
2. Build core adventure mechanics with placeholder art.
3. Standardize kid data schema and hooking it into the loader.
4. Add customization panel (for adults) to assign colors, upload art.
5. Polish tablet controls + accessibility, then finalize GitHub Pages deployment.

## Local Testing
- Keep everything static-friendly so you can open `index.html` directly for quick layout checks.
- For realistic routing and asset loading, run a dev server:
  ```sh
  npm install
  npm run dev        # Vite/Parcel hot reload
  ```
- To preview the production build before pushing to GitHub Pages:
  ```sh
  npm run build
  npx serve dist     # or python -m http.server from /dist
  ```
- Test on tablets via LAN: run `npm run dev -- --host`, hit the machine's IP from the tablet browser.
- Use browser dev tools to throttle network/CPU and simulate touch input before deploying.

## Next Steps Today
- Flesh out `kids.json` structure and sample entry.
- Decide on Phaser vs. pure canvas.
- Mock landing page layout (Figma or rough HTML).
- Prep README instructions for collaborators/parents.

This plan keeps everything static-site friendly so it can live entirely on GitHub Pages, works well on tablets, and scales easily as you add more kids or adventure variants.
