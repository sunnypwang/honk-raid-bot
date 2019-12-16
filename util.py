import discord
import deximage

RAID_STAR = ""
RAID_POKEMON = ""
RAID_OWNER = ""
OWNER_ID = {
    'Sunny' : 'SN',
    'Kirbio' : 'KB',
    'boomngong' : 'BN',
    'BITAH' : 'BT'
}

def generateID(owner, total_posts):
    if owner in OWNER_ID:
        user_id = OWNER_ID[owner]
    else:
        user_id = 'XX'
    post_id = total_posts
    return f'{user_id}{post_id:02d}'

def setCurrentRaidInfo(star,pokemon,owner):
    global RAID_STAR
    global RAID_POKEMON
    global RAID_OWNER
    
    RAID_STAR = star
    RAID_POKEMON = pokemon
    RAID_OWNER = owner
    
async def addRaidResultReact(msg):
    await msg.add_reaction(emoji="\U0001F171") #Emoji B
    await msg.add_reaction(emoji="\U0001F1E8") #Regional Indicator C

def formatResultMessage(caughtlist,brokelist):
    msg = ""
    for user in caughtlist:
        msg = user+" caught the Pokemon!\n"
    for user in brokelist:
        msg = user+" broke.\n"
    if msg=="":
        msg = "There is no result"
    return msg

def getRaidPokemonEmbed(data):
    embed = discord.Embed()

    isgmax = ""

    star = ""

    
    if (data['gmax']):
        isgmax = "G-"
        embed.color = 0xF90195

    for i in range(0,int(data['rarity'])):
        star = star+":star:"
    
    embed.title = isgmax+data['name']
    embed.description = star

    natdexnum = deximage.getSerebiiDirect(data['name'])
    
    embed.set_thumbnail(url="https://www.serebii.net/swordshield/pokemon/"+natdexnum+".png")
    embed.thumbnail.width = 64
    embed.thumbnail.height = 64
    embed.set_author(name=data['owner'])
    
    return embed
