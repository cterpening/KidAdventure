export const DEFAULT_KID_ID = "eli";

export const ASSET_CONFIG = {
  eli: {
    displayName: "Eli",
    assets: {
      player: "assets/kids/eli/player.png",
      dragon: "assets/common/dragon.png",
      dragonDead: "assets/common/dragon-dead.png",
      key: "assets/common/key.png",
      sword: "assets/common/sword.png",
      trophy: "assets/common/trophy.png",
      bat: "assets/common/bat.svg"
    }
  },
  isla: {
    displayName: "Isla",
    assets: {
      player: "assets/kids/isla/player.png",
      dragon: "assets/common/dragon.png",
      dragonDead: "assets/common/dragon-dead.png",
      key: "assets/common/key.png",
      sword: "assets/common/sword.png",
      trophy: "assets/common/trophy.png",
      bat: "assets/common/bat.svg"
    }
  },
  kylie: {
    displayName: "Kylie",
    assets: {
      player: "assets/kids/kylie/player.png",
      dragon: "assets/common/dragon.png",
      dragonDead: "assets/common/dragon-dead.png",
      key: "assets/common/key.png",
      sword: "assets/common/sword.png",
      trophy: "assets/common/trophy.png",
      bat: "assets/common/bat.svg"
    }
  }
};

export const LEVEL_CONFIG = {
  adventure: {
    label: "Adventure Mode",
    description: "Stable, Atari-inspired castle quest.",
    variants: ["classic"]
  },
  remix: {
    label: "Remix Mode",
    description: "Rotates through larger family remix maps.",
    variants: ["shuffled", "labyrinth", "catacombs", "highlands", "gauntlet"]
  }
};

export const DEFAULT_LEVEL_ID = "adventure";

export const ITEM_DEFS = {
  sword: { label: "Sword", color: "#dfe6ef", imageKey: "sword" },
  trophy: { label: "Trophy", color: "#f7b500", imageKey: "trophy" },
  bridge: { label: "Bridge", color: "#8bc6ff", imageKey: null },
  "key-yellow": { label: "Yellow Key", color: "#f6d26a", gateColor: "#d1ac3b", imageKey: "key" },
  "key-black": { label: "Black Key", color: "#9aa0a6", gateColor: "#3b3b3b", imageKey: "key" },
  "key-green": { label: "Green Key", color: "#72e39a", gateColor: "#2b9154", imageKey: "key" },
  "key-white": { label: "White Key", color: "#e8eef8", gateColor: "#cfd8e3", imageKey: "key" },
  key: { label: "Yellow Key", color: "#f6d26a", gateColor: "#d1ac3b", imageKey: "key" }
};
