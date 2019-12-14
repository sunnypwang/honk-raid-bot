import discord
import requests
import raidful as rf
import const
import util

announcementMsg = ''

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global announcementMsg
    if message.author == client.user:

        # if it's the raid announcement msg
        if message.content.startswith('**Raid Announcement**'):
            announcementMsg = message
            await util.addRaidResultReact(message);
        else:
            return

    #Force terminate bot
    if message.content.startswith('!stop'):
        await client.logout()

    elif message.content.startswith('!post'):
        content = message.content.strip().split(" ")
        params = content[1:len(content)]
        if (len(params) > 0):
            res = rf.postRaid(params, message.author.name)
            await message.channel.send(res)
        else:
            await message.channel.send('Please provide Pokemon name (If Gigantamax please include )')


    #Temporary Raid Announcement Test, will think of a proper command+format later
    elif message.content.startswith('!announce'):
        await message.channel.send('**Raid Announcement**\nEPIC')

    #Get latest raid result
    elif message.content.startswith('!result'):
        if announcementMsg=="":
            await message.channel.send("Please start the raid first.")
            return

        #Check for valid emotes
        validemote = ["\U0001F171","\U0001F1E8"];
        brokelist = []
        caughtlist = []
        reactions = announcementMsg.reactions
        
        #Make a list of caught/broke users
        for r in reactions:
            if r.emoji not in validemote:
                pass
            users = await r.users().flatten()
            for u in users:
                if not u == client.user:
                    if r.emoji == "\U0001F171":
                        brokelist.append(u.name);
                    else:
                        if u.name not in brokelist:
                            caughtlist.append(u.name)
                            
        #Clear all reactions on the post, reset the announcement
        await announcementMsg.clear_reactions()
        announcementMsg = ""
                            
        msg = util.formatResultMessage(caughtlist,brokelist)
        await message.channel.send(msg)

    elif message.content.startswith('!list'):
        content = message.content.strip().split(" ")
        parameters = content[1:len(content)]
        if len(parameters)==0:
            data = rf.getAllPokemonList()
            msg = ""
            for i in data:
                await message.channel.send(embed=util.getRaidPokemonEmbed(i))
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
