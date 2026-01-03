from PIL import Image  # pip install pillow
import json
import os
import shutil

# Creates a resource pack and adds all missing items to minecrafts "items" atlas

BASE_DIR = os.path.dirname(__file__)
RESOURCE_PACK_FOLDER = os.path.join(BASE_DIR, "output", "Bingo Icons")
ITEMS_TO_COPY = []


def generate_default_resource_pack():
    pack_mcmeta_file = os.path.join(RESOURCE_PACK_FOLDER, "pack.mcmeta")

    pack_mcmeta = {
        "pack": {
            "description": "Enables Icons for Bingo",
            "min_format": 70,
            "max_format": 75
        }
    }

    # Create the resource pack folder
    os.makedirs(RESOURCE_PACK_FOLDER, exist_ok=True)

    # Write the pack.mcmeta file
    with open(pack_mcmeta_file, "w") as f:
        f.write(json.dumps(pack_mcmeta, indent=4))

    # Copy the pack.png file to the input folder if it exists
    input_pack_png = os.path.join(BASE_DIR, "input", "pack.png")
    if os.path.exists(input_pack_png):
        shutil.copy(input_pack_png, os.path.join(RESOURCE_PACK_FOLDER, "pack.png"))

    # Create the assets folder
    assets_folder = os.path.join(RESOURCE_PACK_FOLDER, "assets", "minecraft")
    os.makedirs(assets_folder, exist_ok=True)


def generate_items_atlas_json():
    items_atlas_file = os.path.join(RESOURCE_PACK_FOLDER, "assets", "minecraft", "atlases", "items.json")
    os.makedirs(os.path.dirname(items_atlas_file), exist_ok=True)

    items_atlas = {
        "sources": [
            {
                "type": "minecraft:directory",
                "prefix": "item/",
                "source": "block_item"
            },
            {
                "type": "minecraft:directory",
                "prefix": "advancement_item/",
                "source": "advancement_item"
            }
        ]
    }

    # Write the items.json file
    with open(items_atlas_file, "w") as f:
        f.write(json.dumps(items_atlas, indent=4))


def copy_icons_from_icon_exporter_mod():
    # Mod: https://modrinth.com/mod/icon-exporter
    # Problems: white_banner is not white but ominous
    input_icons_folder = os.path.join(BASE_DIR, "input", "icon-exports-x16")
    textures_folder = os.path.join(RESOURCE_PACK_FOLDER, "assets", "minecraft", "textures", "block_item")
    os.makedirs(textures_folder, exist_ok=True)

    for item_id in ITEMS_TO_COPY:
        file_name = f"minecraft__{item_id}.png"
        input_file_path = os.path.join(input_icons_folder, file_name)
        if not os.path.exists(input_file_path):
            print(f"Warning: Icon for item '{item_id}' not found ({input_file_path}).")
            continue

        new_file_name = item_id + ".png"
        new_file_path = os.path.join(textures_folder, new_file_name)
        if os.path.exists(new_file_path):
            continue

        shutil.copy(input_file_path, new_file_path)


def get_advancement_items():
    advancement_items = []

    input_advancement_folder = os.path.join(BASE_DIR, "input", "advancement")
    for folder_name in os.listdir(input_advancement_folder):
        if folder_name == "recipes":
            continue
        folder_path = os.path.join(input_advancement_folder, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Load advancements from _all.json
        with open(os.path.join(folder_path, "_all.json"), "r") as f:
            for advancement_name, advancement_data in json.load(f).items():
                advancement_items.append(advancement_data["display"]["icon"]["id"].split(":", 1)[1])

    return list(set(advancement_items))


def generate_advancement_icons():
    # Overlay the background image with each advancement item and save as png
    background_image_path = os.path.join(BASE_DIR, "input", "advancement_background.png")
    input_icons_folder = os.path.join(BASE_DIR, "input", "icon-exports-x16")
    textures_folder = os.path.join(RESOURCE_PACK_FOLDER, "assets", "minecraft", "textures", "advancement_item")
    os.makedirs(textures_folder, exist_ok=True)

    advancement_items = get_advancement_items()
    print(f"Generating advancement icons for {len(advancement_items)} items.")

    for item_id in advancement_items:
        file_name = f"minecraft__{item_id}.png"

        # Special case
        if item_id == "potion":
            file_name = "minecraft__potion__{'minecraft__potion_contents'__{potion__'minecraft__water'}}.png"

        input_file_path = os.path.join(input_icons_folder, file_name)
        if not os.path.exists(input_file_path):
            print(f"Warning: Icon for advancement item '{item_id}' not found ({input_file_path}).")
            continue

        new_file_name = item_id + ".png"
        new_file_path = os.path.join(textures_folder, new_file_name)
        if os.path.exists(new_file_path):
            continue

        # Create the advancement icon by overlaying the background and the item icon
        background = Image.open(background_image_path).convert("RGBA").resize((22, 22))
        item_icon = Image.open(input_file_path).convert("RGBA")

        # Center the item icon on the background
        position = ((background.width - item_icon.width) // 2, (background.height - item_icon.height) // 2)
        background.paste(item_icon, position, item_icon)

        background.save(new_file_path)


def generate_bingo_advancement_item_models():
    textures_folder = os.path.join(RESOURCE_PACK_FOLDER, "assets", "minecraft", "textures", "advancement_item")
    items_folder = os.path.join(RESOURCE_PACK_FOLDER, "assets", "bingo", "items")
    models_folder = os.path.join(RESOURCE_PACK_FOLDER, "assets", "bingo", "models", "item")
    os.makedirs(items_folder, exist_ok=True)
    os.makedirs(models_folder, exist_ok=True)

    for filename in os.listdir(textures_folder):
        if not filename.endswith(".png"):
            continue

        item_id = filename.replace(".png", "")

        # /assets/bingo/items/{item_id}_advancement.json
        item_items_file = os.path.join(items_folder, f"{item_id}_advancement.json")
        if not os.path.exists(item_items_file):
            with open(item_items_file, "w") as f:
                f.write(json.dumps({
                    "model": {
                        "type": "minecraft:model",
                        "model": f"bingo:item/{item_id}_advancement"
                    }
                }, indent=4))

        # /assets/bingo/models/item/{item_id}_advancement.json
        item_models_file = os.path.join(models_folder, f"{item_id}_advancement.json")
        if not os.path.exists(item_models_file):
            with open(item_models_file, "w") as f:
                f.write(json.dumps({
                    "parent": "minecraft:item/generated",
                    "textures": {
                        "layer0": f"minecraft:advancement_item/{item_id}"
                    }
                }, indent=4))


if __name__ == "__main__":
    generate_default_resource_pack()
    generate_items_atlas_json()
    copy_icons_from_icon_exporter_mod()
    generate_advancement_icons()
    generate_bingo_advancement_item_models()
