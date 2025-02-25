# Minecraft Bingo Resource Pack
Resource Pack for https://github.com/170yt/Minecraft-Bingo

The server can be configured to prompt the player to download the resource pack when they join the server.
I uploaded the resource pack to [mc-packs.net](https://download.mc-packs.net/pack/4d20d1635481eb40bf4ce0d7726468457374c917.zip).
To use it, add the following lines to the server.properties file:
```
resource-pack=https://download.mc-packs.net/pack/4d20d1635481eb40bf4ce0d7726468457374c917.zip
resource-pack-sha1=4d20d1635481eb40bf4ce0d7726468457374c917
```
The resource pack can also be downloaded from [Modrinth](TODO: add link).
A file with all mappings between item names and icons can be found [here](https://github.com/170yt/Minecraft-Bingo-Resource-Pack) and must be placed in `config/bingo/item_icon_mappings.json`.
All icons will be disabled if the mappings file is not provided.
