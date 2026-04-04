# KidAdventure Direction

This document captures the current product direction for KidAdventure. It replaces the older prototype-plan assumptions about routers, build tooling, `kids.json`, and optional engine swaps.

## Core Goal
- Deliver a game that feels recognizably like Atari 2600 Adventure.
- Keep the original-style loop readable for kids and adults: one carried item, keys and castles, sword and dragons, bat interference, trophy return.
- Use family-specific player art and stronger room/icon presentation to make it feel warmer and more polished than a literal clone.

## Experience Rules
- The default mode should be teachable and stable.
- Surprise should come from enemy pressure, item recovery, and optional remix worlds, not from making the base map unreadable.
- Visual upgrades should improve clarity first and novelty second.

## Mode Strategy
1. `Adventure Mode`
- Single dependable overworld.
- Closest match to the original game's learning loop.
- Best choice for first-time players and younger players.

2. `Remix Mode`
- Uses the same rule set and core objects.
- Rotates through larger authored maps after players understand the classic loop.
- Lets the project explore more dramatic spaces without weakening the main identity.

## Art Strategy
- Keep family photos or drawings only for the player characters.
- Keep item silhouettes strong enough to read at a glance.
- Use castle silhouettes, room names, and stronger map landmarks to create personality without losing navigational clarity.

## Implementation Notes
- `js/content-config.js` owns kid and mode configuration.
- `js/game.js` owns the runtime, rendering, and authored maps.
- The project stays static-site friendly and does not require a build step.
- Validation stays lightweight and dependency-free through the Python scripts in `tools/`.

## Next Improvement Targets
- Tighten the classic map further if specific rooms still feel too maze-heavy.
- Give dragons slightly more distinct personalities without breaking fairness.
- Replace more placeholder/common item art over time now that the icon language is clearer.
- Add browser-level smoke testing if the project grows beyond the current single-file runtime approach.
