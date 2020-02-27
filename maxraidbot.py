import discord
import requests
import raidful
import const
import util


def parse_parameters(content):
    return content.strip().lower().split()[1:]


raid_message_id = None
raid_start = False
client = discord.Client()
DELAY = 3


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

    print(message.content)
    params = parse_parameters(message.content)
    # user message
    if message.content.startswith('!logout'):
        if not message.content.startswith('!logout force'):
            print(raidful.closeRaid())
            # print(deleteAllRaid)

        await client.logout()

    elif message.content.startswith('!list'):
        # await message.channel.send('Here is all available raids')
        emb_raids = raidful.listRaid(params)
        if emb_raids:
            for emb_raid in emb_raids:
                await message.channel.send(embed=emb_raid)
        else:
            await message.channel.send('There is no Pokemon on the list.')

    elif message.content.startswith('!post'):
        await message.channel.send('Posting new raid...', delete_after=DELAY)
        res = raidful.postRaid(params, message.author.name)
        await message.channel.send(res['msg'])

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

        else:
            await message.channel.send(res['msg'])

    elif message.content.startswith('!close'):
        await message.channel.send('Ending raid...', delete_after=DELAY)
        res = raidful.closeRaid()
        raid_start = False
        await message.channel.send(res, delete_after=DELAY)

    elif message.content.startswith('!clear'):
        await message.channel.send('Deleting... Please kindly sit tight', delete_after=DELAY*2)
        res = raidful.deleteRaid(params, message.author.name)
        raid_start = False
        await message.channel.send(res)

    elif message.content.startswith('!flush'):
        await message.channel.send('Deleting... Please kindly sit tight for a while', delete_after=DELAY*3)
        res = raidful.deleteAllRaid()
        raid_start = False
        await message.channel.send(res)

    # Get latest raid result
    elif message.content.startswith('!result'):
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

client.run(const.BOT_TOKEN)
