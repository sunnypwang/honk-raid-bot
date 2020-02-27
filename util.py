import discord
import deximage

RAID_STAR = ""
RAID_POKEMON = ""
RAID_OWNER = ""
OWNER_ID = {
    'Sunny': 'SN',
    'Kirbio': 'KB',
    'boomngong': 'BN',
    'BITAH': 'BT'
}


def generateID(owner, total_posts):
    if owner in OWNER_ID:
        user_id = OWNER_ID[owner]
    else:
        user_id = 'XX'
    post_id = total_posts
    return f'{user_id}{post_id:02d}'


def setCurrentRaidInfo(star, pokemon, owner):
    global RAID_STAR
    global RAID_POKEMON
    global RAID_OWNER

    RAID_STAR = star
    RAID_POKEMON = pokemon
    RAID_OWNER = owner


async def addRaidResultReact(msg):
    await msg.add_reaction(emoji="\U0001F171")  # Emoji B
    await msg.add_reaction(emoji="\U0001F1E8")  # Regional Indicator C


def formatPokemon(raid):
    gmax_prefix = "G-" if raid['gmax'] else ""
    return "{:d} Star {}{}".format(raid['rarity'], gmax_prefix, raid['pokemon'].capitalize())


def formatResultMessage(caughtlist, brokelist):
    msg = ""
    for user in caughtlist:
        msg = user+" caught the Pokemon!\n"
    for user in brokelist:
        msg = user+" broke.\n"
    if msg == "":
        msg = "There is no result"
    return msg


def embedRaid(raid):
    embed = discord.Embed()

    gmax_prefix = "G-" if raid['gmax'] else ""
    star = ':star:' * int(raid['rarity'])
    embed.color = 0xA41CFF if raid['gmax'] else 0xF90195
    embed.title = gmax_prefix + raid['pokemon'].capitalize()
    # if raid['code'] != '':
    #     embed.description = '{}\n\n`{:4d}`'.format(star, int(raid['#']))
    # else:
    #     embed.description = '{}'.format(star)
    embed.add_field(name='ID', value='{}'.format(raid['#']))
    embed.add_field(name='passcode', value='{}'.format(raid['code']))
    embed.set_thumbnail(
        url=deximage.getThumbnailURL(raid['pokemon']))
    embed.thumbnail.width = 64
    embed.thumbnail.height = 64
    # embed.set_author(name=raid['owner'])

    return embed


def embedRaidList(raids):
    embeds = []
    for raid in raids:
        embeds.append(embedRaid(raid))
    return embeds
