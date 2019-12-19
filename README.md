# honk-raid-bot

Discord bot for Pokemon Sword & Shield Raid Announcement

Features:
- `list` for listing all available raids
- `post <NAME> [RARITY] [isGMAX]` for posting new raid (if rarity is not specified it defaults to 5, owner could be extracted from message object)
- `start <ID> [CODE]` for announcing a room to start the raid
- `clear <ID>` for clearing all raids from that owner with given name . If <ID> is all then clear all raids from that owner
- `flush` for clearing every single raid
- `toggle <ID>` for enabling/disabling specific raid (assuming no duplicate mons)
