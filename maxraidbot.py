import discord
import raidful as rf
import const

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
    embed.set_thumbnail(url="https://www.serebii.net/swordshield/pokemon/132.png")
    embed.thumbnail.width = 64
    embed.thumbnail.height = 64
    embed.set_author(name=data['owner'])
    
    return embed

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!getraidlist'):
        content = message.content.strip().split(" ")
        parameters = content[1:len(content)]
        if len(parameters)==0:
            data = rf.getAllPokemonList()
            msg = ""
            for i in data:
                await message.channel.send(embed=getRaidPokemonEmbed(i))
                #msg = msg+rf.formatPokemon(i)+"\n"
            '''if msg=="":
                 await message.channel.send('There is no Pokemon on the list.')
            else:
                 await message.channel.send(msg)'''
        else:
            data = rf.getUserPokemonList(parameters[0])
            msg = ""
            for i in data:
                msg = msg+rf.formatPokemon(i)+"\n"
            if msg=="":
                 await message.channel.send('There is no Pokemon on the list.')
            else:
                 await message.channel.send(msg)

client.run(const.BOT_TOKEN)
