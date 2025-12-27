import json
import os
import shutil


def generate_default_resource_pack(base_dir, resource_pack_folder, pack_format, pack_description):
    pack_mcmeta_file = os.path.join(resource_pack_folder, "pack.mcmeta")

    pack_mcmeta = {
        "pack": {
            "pack_format": pack_format,
            "description": pack_description
        }
    }

    # Create the resource pack folder
    os.makedirs(resource_pack_folder, exist_ok=True)

    # Write the pack.mcmeta file
    with open(pack_mcmeta_file, "w") as f:
        f.write(json.dumps(pack_mcmeta, indent=2))
    
    # Copy the pack.png file to the input folder if it exists
    input_pack_png = os.path.join(base_dir, "input", "pack.png")
    if os.path.exists(input_pack_png):
        shutil.copy(input_pack_png, os.path.join(resource_pack_folder, "pack.png"))

    # Create the assets folder
    assets_folder = os.path.join(resource_pack_folder, "assets", "minecraft")
    os.makedirs(assets_folder, exist_ok=True)


def copy_icons_from_icon_exporter_mod(base_dir, resource_pack_folder):
    # Mod: https://modrinth.com/mod/icon-exporter
    # Sort out unwanted icons
    input_icons_folder = os.path.join(base_dir, "input", "icon-exports-x16")
    textures_folder = os.path.join(resource_pack_folder, "assets", "minecraft", "textures", "icons")
    os.makedirs(textures_folder, exist_ok=True)

    for file_name in os.listdir(input_icons_folder):
        if not file_name.endswith(".png"):
            continue

        # Sort out fluids
        if file_name.startswith("fluid__"):
            continue

        # Sort out items with NBT data
        # if "{" in file_name:
        #     continue

        item_id = file_name.split("__")[1].replace(".png", "")
        new_file_name = item_id + ".png"

        new_file_path = os.path.join(textures_folder, new_file_name)
        if os.path.exists(new_file_path):
            continue

        shutil.copy(os.path.join(input_icons_folder, file_name), new_file_path)


def get_advancements_per_category(base_dir):
    advancements = {}

    input_advancement_folder = os.path.join(base_dir, "input", "advancement")
    for folder_name in os.listdir(input_advancement_folder):
        if folder_name == "recipes":
            continue
        folder_path = os.path.join(input_advancement_folder, folder_name)
        if not os.path.isdir(folder_path):
            continue

        advancements[folder_name] = []

        # Load advancements from _all.json
        with open(os.path.join(folder_path, "_all.json"), "r") as f:
            for advancement_name, advancement_data in json.load(f).items():
                advancements[folder_name].append({
                    "name": advancement_name,
                    "item": advancement_data["display"]["icon"]["id"].split(":", 1)[1],
                    # Frame could be used to set the proper background for the item
                    # "frame": advancement_data["display"]["frame"] if "frame" in advancement_data["display"] else "task"
                })

    return advancements


def generate_advancement_item_models(base_dir, resource_pack_folder, pack_namespace, advancements_per_category):
    ADVANCEMENT_ITEM_MODEL = "bingo:item/advancement"

    items_folder = os.path.join(resource_pack_folder, "assets", pack_namespace, "items")
    os.makedirs(items_folder, exist_ok=True)

    # Load _all.json from the minecraft assets folder
    minecraft_item_assets = os.path.join(base_dir, "input", "assets", "minecraft", "items", "_all.json")
    with open(minecraft_item_assets, "r") as f:
        item_assets = json.load(f)
    print(f"Loaded {len(item_assets)} item assets")

    for category, advancements in advancements_per_category.items():
        print(f"Generating item models for {category} ({len(advancements)} advancements)")
        for advancement in advancements:
            item_advancement_file = os.path.join(items_folder, f"{advancement['item']}_advancement.json")
            if os.path.exists(item_advancement_file):
                # print(f"  Skipping {advancement['item']} as it already exists")
                continue

            with open(item_advancement_file, "w") as f:
                f.write(json.dumps({
                    "model": {
                        "type": "minecraft:composite",
                        "models": [
                            {
                                "type": "minecraft:model",
                                "model": ADVANCEMENT_ITEM_MODEL
                            },
                            # {
                            #     "type": "minecraft:model",
                            #     "model": "minecraft:item/" + advancement["item"]
                            # }
                            item_assets[advancement["item"]]["model"]
                        ]
                    }
                }, indent=2))


def copy_advancement_icons_from_icon_exporter_mod(base_dir, resource_pack_folder, advancements_per_category):
    # Get a list of all items (without duplicates)
    items = []
    for category, advancements in advancements_per_category.items():
        for advancement in advancements:
            items.append(advancement['item'])
    items = list(set(items))

    # Sort out unwanted icons
    input_icons_folder = os.path.join(base_dir, "input", "icon-exports-x16-advancements")
    output_folder = os.path.join(resource_pack_folder, "assets", "minecraft", "textures", "icons")
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_icons_folder):
        if not file_name.endswith(".png"):
            continue

        # Sort out fluids
        if file_name.startswith("fluid__"):
            continue

        item_id = file_name.split("__")[1].replace(".png", "")

        if item_id not in items:
            continue

        new_file_name = item_id + "_advancement.png"

        new_file_path = os.path.join(output_folder, new_file_name)
        if os.path.exists(new_file_path):
            continue

        shutil.copy(os.path.join(input_icons_folder, file_name), new_file_path)


def get_items_from_path(path_to_icons):
    items = {}
    for file_name in os.listdir(path_to_icons):
        if not file_name.endswith(".png"):
            continue

        item_id = file_name.replace(".png", "")
        items[item_id] = "icons/" + file_name

    return items


def generate_font_file_and_mapping(base_dir, resource_pack_folder):
    START_UNICODE_CHARACTER = 0xE000
    ICON_HEIGHT = 10
    ICON_ASCENT = 9

    resource_pack_assets_folder = os.path.join(resource_pack_folder, "assets", "minecraft")
    font_folder = os.path.join(resource_pack_assets_folder, "font")
    font_file = os.path.join(font_folder, "default.json")
    mappings_file = os.path.join(base_dir, "output", "item_icon_mappings.json")

    items = get_items_from_path(os.path.join(resource_pack_assets_folder, "textures", "icons"))

    providers = []
    mappings = {}

    for item_id, file_name in items.items():
        unicode_char = chr(START_UNICODE_CHARACTER + len(providers))
        providers.append({
            "type": "bitmap",
            "file": file_name,
            "height": ICON_HEIGHT,
            "ascent": ICON_ASCENT,
            "chars": [unicode_char]
        })
        mappings[item_id] = unicode_char

    font = {
        "providers": providers
    }

    os.makedirs(font_folder, exist_ok=True)
    with open(font_file, "w") as f:
        f.write(json.dumps(font, indent=2))
    print(f"Wrote {len(items)} items to {font_file}")

    with open(mappings_file, "w") as f:
        f.write(json.dumps(mappings, indent=2))
    print(f"Wrote {len(items)} mappings to {mappings_file}")
