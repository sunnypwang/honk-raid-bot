import discord
import raidful
import const
import util
import asyncio

client = discord.Client()

raid_message_id = None
raid_start = False
DELAY = 3

# Keep track of the latest opened raid
LAST_RAID = {'param': [], 'owner': "-"}


def parse_parameters(content):
    return content.strip().lower().split()[1:]


async def sync_db():
    await client.wait_until_ready()
    while True:
        await asyncio.sleep(600)  # task runs every x seconds
        print('Background sync in progress...')
        raidful.updateRemote()


@client.event
async def on_connect():
    raidful.updateLocal()
    client.loop.create_task(sync_db())


@client.event
async def on_disconnect():
    print('Disconnected')


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global raid_message_id, raid_start
    # bot message
    if message.author == client.user:
        return
        # if it's the raid announcement msg
        # if message.content.startswith('**Raid Announcement**'):
        #     announcementMsg = message
        #     await util.addRaidResultReact(message)
        # else:
        #     return

    # print(message.content)
    params = parse_parameters(message.content)

    if message.content.startswith('!list'):
        # await message.channel.send('Here is all available raids')
        emb_raids = raidful.listRaids(params)
        if emb_raids:
            for emb_raid in emb_raids:
                await message.channel.send(embed=emb_raid)
        else:
            await message.channel.send('There is no Pokemon on the list.')

    elif message.content.startswith('!post'):
        await message.channel.send('Posting new raid...', delete_after=DELAY)
        res = raidful.postRaid(params, message.author.name)
        await message.channel.send(res)

    elif message.content.startswith('!open') or message.content.startswith('!start'):
        await message.channel.send('Starting raid...', delete_after=DELAY)
        res = raidful.openRaid(params, raid_start, message.author.name)
        if res['status'] == 'ok':
            raid_start = True
            await message.channel.send('**RAID ANNOUNCEMENT**')
            msg = await message.channel.send(embed=res['embed'])

            # await util.addRaidResultReact(msg)
            await msg.add_reaction(emoji="\U0001F171")  # Emoji B
            await msg.add_reaction(emoji="\U0001F1E8")  # Regional Indicator C
            raid_message_id = msg.id

            # Set active raid as the latest raid
            LAST_RAID['params'] = params
            LAST_RAID['owner'] = message.author.name.lower()

            # Change status to active raid
            await util.setRaidStatusMessage(client, util.formatPokemon(res['raid']))

        else:
            await message.channel.send(res['msg'])

    elif message.content.startswith('!reopen') or message.content.startswith('!uno') or message.content.startswith('!again') or message.content.startswith('!um') or message.content.startswith('!unomas'):
        if LAST_RAID['owner'] == '-':
            await message.channel.send('There was no latest raid.')
            return

        await message.channel.send('Starting raid...', delete_after=DELAY)
        raid_start = False      #
        res = raidful.openRaid(LAST_RAID['params'],
                               raid_start,
                               LAST_RAID['owner'])
        if res['status'] == 'ok':
            raid_start = True
            await message.channel.send('**RAID ANNOUNCEMENT**')
            msg = await message.channel.send(embed=res['embed'])

            # await util.addRaidResultReact(msg)
            await msg.add_reaction(emoji="\U0001F171")  # Emoji B
            await msg.add_reaction(emoji="\U0001F1E8")  # Regional Indicator C
            raid_message_id = msg.id

            # Change status to active raid
            await util.setRaidStatusMessage(client, util.formatPokemon(res['raid']))

        else:
            await message.channel.send(res['msg'])

    # elif message.content.startswith('!close'):
    #    await message.channel.send('Ending raid...', delete_after=DELAY)
    #    res = raidful.closeRaid()
    #    raid_start = False
    #    await message.channel.send(res, delete_after=DELAY)
    #    #Return status to normal
    #    await util.setRaidStatusMessage(client,"")

    elif message.content.startswith('!clear'):
        await message.channel.send('Deleting... Please kindly sit tight', delete_after=DELAY)
        res = raidful.deleteRaid(params, message.author.name)
        if raid_start:
            raid_start = False
            # Return status to normal
            await util.setRaidStatusMessage(client, "")
            
        await message.channel.send(res)

    elif message.content.startswith('!flush'):
        if util.isAdminMessage(message):
            await message.channel.send('Deleting... Please kindly sit tight for a while', delete_after=DELAY)
            res = raidful.deleteAllRaid()
            if raid_start:
                raid_start = False
                # Return status to normal
                await util.setRaidStatusMessage(client, "")
            
            await message.channel.send(res)
        else:
            await message.channel.send('This command can only be invoked by administrator.\nPlease call @Kirbio or @Sunny for help.')

    # Get latest raid result
    elif message.content.startswith('!result') or message.content.startswith('!close') or message.content.startswith('!end'):
        if not raid_start:
            await message.channel.send("Please start the raid first.")
            return

        # close automatically
        await message.channel.send('Ending raid...', delete_after=DELAY)
        res = raidful.closeRaid()
        raid_start = False

        await message.channel.send('Obtaining result...', delete_after=DELAY)
        # Check for valid emotes
        validemote = ["\U0001F171", "\U0001F1E8"]
        brokelist = []
        caughtlist = []
        raid_msg = await message.channel.fetch_message(raid_message_id)
        reactions = raid_msg.reactions
        # Make a list of caught/broke users
        for r in reactions:
            if r.emoji not in validemote:
                pass
            users = await r.users().flatten()
            for u in users:
                if not u == client.user:
                    if r.emoji == "\U0001F171":
                        brokelist.append(u.name)
                    else:
                        if u.name not in brokelist:
                            caughtlist.append(u.name)

        # Clear all reactions on the post, reset the announcement
        await raid_msg.remove_reaction("\U0001F171", client.user)
        await raid_msg.remove_reaction("\U0001F1E8", client.user)

        raid_message_id = None

        msg = util.formatResultMessage(caughtlist, brokelist)
        await message.channel.send(msg)

        # Return status to normal
        await util.setRaidStatusMessage(client, "")

    elif message.content.startswith('!logout'):
        if not util.isAdminMessage(message):
            await message.channel.send('This command can only be invoked by administrator.\nPlease call @Kirbio or @Sunny for help.')
        else:
            if not message.content.startswith('!logout force'):
                print(raidful.closeRaid())
                raidful.updateRemote()
            await client.logout()

    # sync remote google docs
    elif message.content.startswith('!sync'):
        await message.channel.send('Syncing... (It could take up to a minute)', delete_after=DELAY)
        raidful.updateRemote()
        await message.channel.send('Sync completed', delete_after=DELAY)

    # Simple test command to check if the bot is not dead
    elif message.content.startswith('!ping'):
        await message.channel.send('pong')

    elif message.content.startswith('!local'):
        raidful.logLocalRaids()

    # test setting status message
    elif message.content.startswith('!test'):
        if util.isAdminMessage(message):
            print('This admin message')
        else:
            print('This not admin message')

client.run(const.BOT_TOKEN)
