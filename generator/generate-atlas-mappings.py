import json
import os

# To generate the input file, press F3+S in Minecraft.
# Go to .minecraft/screenshots/debug and put the below INPUT_FILE in this input folder.

BASE_DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(BASE_DIR, "input", "minecraft_textures_atlas_items.png.txt")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "atlas_mappings.json")

BLACKLISTED_SUFFIXES = [
    "bundle_open_back",
    "bundle_open_front",
    "_spear_in_hand",
    "_overlay",
    "/crossbow_arrow",
    "/crossbow_firework",
    "/crossbow_standby",
    "/elytra_broken",
    "/filled_map_markings",
    "/fishing_rod_cast",
    "/spyglass_model",
    "/tipped_arrow_base",
    "/tipped_arrow_head",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
]
SPECIAL_ITEMS = {
    "minecraft:clock": "item/clock_00",
    "minecraft:compass": "item/compass_20",
    "minecraft:crossbow": "item/crossbow_standby",
    "minecraft:disc_fragment_5": "item/disc_fragment_5",
    "minecraft:music_disc_5": "item/music_disc_5",
    "minecraft:music_disc_11": "item/music_disc_11",
    "minecraft:music_disc_13": "item/music_disc_13",
    "minecraft:recovery_compass": "item/recovery_compass_20",
    "minecraft:tipped_arrow": "item/arrow",
}


def generate_atlas_mappings():
    atlas_mappings = SPECIAL_ITEMS.copy()

    with open(INPUT_FILE, "r") as f:
        lines = f.readlines()
        for line in lines:
            value = line.split("\t", 1)[0]

            if not value.startswith("minecraft:item/"):
                continue
            if any(value.endswith(suffix) for suffix in BLACKLISTED_SUFFIXES):
                continue

            item = value.replace("item/", "")
            sprite = value.split(":", 1)[-1]

            atlas_mappings[item] = sprite

    print(f"Generated {len(atlas_mappings)} atlas mappings.")
    return atlas_mappings


def save_atlas_mappings_to_json(atlas_mappings):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(atlas_mappings, f, indent=4)


def atlas_mappings_to_java_hashmap(atlas_mappings):
    for item, sprite in atlas_mappings.items():
        print(f'        sprites.put(Items.{item.replace("minecraft:", "").upper()}, "{sprite}");')


if __name__ == "__main__":
    atlas_mappings = generate_atlas_mappings()
    save_atlas_mappings_to_json(atlas_mappings)
    # atlas_mappings_to_java_hashmap(atlas_mappings)
