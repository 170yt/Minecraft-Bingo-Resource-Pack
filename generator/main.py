import os
from .generator import generate_default_resource_pack, copy_icons_from_icon_exporter_mod, get_advancements_per_category, generate_advancement_item_models, copy_advancement_icons_from_icon_exporter_mod, generate_font_file_and_mapping


RESOURCE_PACK_NAME = "Bingo Icons"
RESOURCE_PACK_DESCRIPTION = "Enables Icons for Bingo"
RESOURCE_PACK_FORMAT = 46
RESOURCE_PACK_NAMESPACE = "bingo"


BASE_DIR = os.path.dirname(__file__)
RESOURCE_PACK_FOLDER = os.path.join(BASE_DIR, "output", RESOURCE_PACK_NAME)


generate_default_resource_pack(BASE_DIR, RESOURCE_PACK_FOLDER, RESOURCE_PACK_FORMAT, RESOURCE_PACK_DESCRIPTION)
copy_icons_from_icon_exporter_mod(BASE_DIR, RESOURCE_PACK_FOLDER)
advancements = get_advancements_per_category(BASE_DIR)
generate_advancement_item_models(BASE_DIR, RESOURCE_PACK_FOLDER, RESOURCE_PACK_NAMESPACE, advancements)
copy_advancement_icons_from_icon_exporter_mod(BASE_DIR, RESOURCE_PACK_FOLDER, advancements)
generate_font_file_and_mapping(BASE_DIR, RESOURCE_PACK_FOLDER)
