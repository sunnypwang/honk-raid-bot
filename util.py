import discord
from difflib import get_close_matches

dexlist = {'grookey': '810', 'thwackey': '811', 'rillaboom': '812', 'scorbunny': '813', 'raboot': '814', 'cinderace': '815', 'sobble': '816', 'drizzile': '817', 'inteleon': '818', 'blipbug': '824', 'dottler': '825', 'orbeetle': '826', 'caterpie': '010', 'metapod': '011', 'butterfree': '012', 'grubbin': '736', 'charjabug': '737', 'vikavolt': '738', 'hoothoot': '163', 'noctowl': '164', 'rookidee': '821', 'corvisquire': '822', 'corviknight': '823', 'skwovet': '819', 'greedent': '820', 'pidove': '519', 'tranquill': '520', 'unfezant': '521', 'nickit': '827', 'thievul': '828', 'zigzagoon': '263-g', 'linoone': '264-g', 'obstagoon': '862', 'wooloo': '831', 'dubwool': '832', 'lotad': '270', 'lombre': '271', 'ludicolo': '272', 'seedot': '273', 'nuzleaf': '274', 'shiftry': '275', 'chewtle': '833', 'drednaw': '834', 'purrloin': '509', 'liepard': '510', 'yamper': '835', 'boltund': '836', 'bunnelby': '659', 'diggersby': '660', 'minccino': '572', 'cinccino': '573', 'bounsweet': '761', 'steenee': '762', 'tsareena': '763', 'oddish': '043', 'gloom': '044', 'vileplume': '045', 'bellossom': '182', 'budew': '406', 'roselia': '315', 'roserade': '407', 'wingull': '278', 'pelipper': '279', 'joltik': '595', 'galvantula': '596', 'electrike': '309', 'manectric': '310', 'vulpix': '037', 'ninetales': '038', 'growlithe': '058', 'arcanine': '059', 'vanillite': '582', 'vanillish': '583', 'vanilluxe': '584', 'swinub': '220', 'piloswine': '221', 'mamoswine': '473', 'delibird': '225', 'snorunt': '361', 'glalie': '362', 'froslass': '478', 'baltoy': '343', 'claydol': '344', 'mudbray': '749', 'mudsdale': '750', 'dwebble': '557', 'crustle': '558', 'golett': '622', 'golurk': '623', 'munna': '517', 'musharna': '518', 'natu': '177', 'xatu': '178', 'stufful': '759', 'bewear': '760', 'snover': '459', 'abomasnow': '460', 'krabby': '098', 'kingler': '099', 'wooper': '194', 'quagsire': '195', 'corphish': '341', 'crawdaunt': '342', 'nincada': '290', 'ninjask': '291', 'shedinja': '292', 'tyrogue': '236', 'hitmonlee': '106', 'hitmonchan': '107', 'hitmontop': '237', 'pancham': '674', 'pangoro': '675', 'klink': '599', 'klang': '600', 'klinklang': '601', 'combee': '415', 'vespiquen': '416', 'bronzor': '436', 'bronzong': '437', 'ralts': '280', 'kirlia': '281', 'gardevoir': '282', 'gallade': '475', 'drifloon': '425', 'drifblim': '426', 'gossifleur': '829', 'eldegoss': '830', 'cherubi': '420', 'cherrim': '421', 'stunky': '434', 'skuntank': '435', 'tympole': '535', 'palpitoad': '536', 'seismitoad': '537', 'duskull': '355', 'dusclops': '356', 'dusknoir': '477', 'machop': '066', 'machoke': '067', 'machamp': '068', 'gastly': '092', 'haunter': '093', 'gengar': '094', 'magikarp': '129', 'gyarados': '130', 'goldeen': '118', 'seaking': '119', 'remoraid': '223', 'octillery': '224', 'shellder': '090', 'cloyster': '091', 'feebas': '349', 'milotic': '350', 'basculin': '550-b', 'wishiwashi': '746', 'pyukumuku': '771', 'trubbish': '568', 'garbodor': '569', 'sizzlipede': '850', 'centiskorch': '851', 'rolycoly': '837', 'carkol': '838', 'coalossal': '839', 'diglett': '050', 'dugtrio': '051', 'drilbur': '529', 'excadrill': '530', 'roggenrola': '524', 'boldore': '525', 'gigalith': '526', 'timburr': '532', 'gurdurr': '533', 'conkeldurr': '534', 'woobat': '527', 'swoobat': '528', 'noibat': '714', 'noivern': '715', 'onix': '095', 'steelix': '208', 'arrokuda': '846', 'barraskewda': '847', 'meowth': '052', 'perrserker': '863', 'persian': '053', 'milcery': '868', 'alcremie': '869', 'cutiefly': '742', 'ribombee': '743', 'ferroseed': '597', 'ferrothorn': '598', 'pumpkaboo': '710', 'gourgeist': '711', 'pichu': '172', 'pikachu': '025', 'raichu': '026', 'eevee': '133', 'vaporeon': '134', 'jolteon': '135', 'flareon': '136', 'espeon': '196', 'umbreon': '197', 'leafeon': '470',
           'glaceon': '471', 'sylveon': '700', 'applin': '840', 'flapple': '841', 'appletun': '842', 'espurr': '677', 'meowstic': '678-f', 'swirlix': '684', 'slurpuff': '685', 'spritzee': '682', 'aromatisse': '683', 'dewpider': '751', 'araquanid': '752', 'wynaut': '360', 'wobbuffet': '202', "farfetch'd": '083-g', "sirfetch'd": '865', 'chinchou': '170', 'lanturn': '171', 'croagunk': '453', 'toxicroak': '454', 'scraggy': '559', 'scrafty': '560', 'stunfisk': '618-g', 'shuckle': '213', 'barboach': '339', 'whiscash': '340', 'shellos': '422-e', 'gastrodon': '423-e', 'wimpod': '767', 'golisopod': '768', 'binacle': '688', 'barbaracle': '689', 'corsola': '222-g', 'cursola': '864', 'impidimp': '859', 'morgrem': '860', 'grimmsnarl': '861', 'hatenna': '856', 'hattrem': '857', 'hatterene': '858', 'salandit': '757', 'salazzle': '758', 'pawniard': '624', 'bisharp': '625', 'throh': '538', 'sawk': '539', 'koffing': '109', 'weezing': '110-g', 'bonsly': '438', 'sudowoodo': '185', 'cleffa': '173', 'clefairy': '035', 'clefable': '036', 'togepi': '175', 'togetic': '176', 'togekiss': '468', 'munchlax': '446', 'snorlax': '143', 'cottonee': '546', 'whimsicott': '547', 'rhyhorn': '111', 'rhydon': '112', 'rhyperior': '464', 'gothita': '574', 'gothorita': '575', 'gothitelle': '576', 'solosis': '577', 'duosion': '578', 'reuniclus': '579', 'karrablast': '588', 'escavalier': '589', 'shelmet': '616', 'accelgor': '617', 'elgyem': '605', 'beheeyem': '606', 'cubchoo': '613', 'beartic': '614', 'rufflet': '627', 'braviary': '628', 'vullaby': '629', 'mandibuzz': '630', 'skorupi': '451', 'drapion': '452', 'litwick': '607', 'lampent': '608', 'chandelure': '609', 'inkay': '686', 'malamar': '687', 'sneasel': '215', 'weavile': '461', 'sableye': '302', 'mawile': '303', 'maractus': '556', 'sigilyph': '561', 'riolu': '447', 'lucario': '448', 'torkoal': '324', 'mimikyu': '778', 'cufant': '878', 'copperajah': '879', 'qwilfish': '211', 'frillish': '592', 'jellicent': '593', 'mareanie': '747', 'toxapex': '748', 'cramorant': '845', 'toxel': '848', 'toxtricity': '849-l', 'silicobra': '843', 'sandaconda': '844', 'hippopotas': '449', 'hippowdon': '450', 'durant': '632', 'heatmor': '631', 'helioptile': '694', 'heliolisk': '695', 'hawlucha': '701', 'trapinch': '328', 'vibrava': '329', 'flygon': '330', 'axew': '610', 'fraxure': '611', 'haxorus': '612', 'yamask': '562', 'runerigus': '867', 'cofagrigus': '563', 'honedge': '679', 'doublade': '680', 'aegislash': '681', 'ponyta': '077-g', 'rapidash': '078-g', 'sinistea': '854', 'polteageist': '855', 'indeedee': '876-f', 'phantump': '708', 'trevenant': '709', 'morelull': '755', 'shiinotic': '756', 'oranguru': '765', 'passimian': '766', 'morpeko': '877', 'falinks': '870', 'drampa': '780', 'turtonator': '776', 'togedemaru': '777', 'snom': '872', 'frosmoth': '873', 'clobbopus': '852', 'grapploct': '853', 'pincurchin': '871', 'mantyke': '458', 'mantine': '226', 'wailmer': '320', 'wailord': '321', 'bergmite': '712', 'avalugg': '713', 'dhelmise': '781', 'lapras': '131', 'lunatone': '337', 'solrock': '338', 'mime jr.': '439', 'mr. mime': '122-g', 'mr. rime': '866', 'darumaka': '554-g', 'darmanitan': '555-g', 'stonjourner': '874', 'eiscue': '875', 'duraludon': '884', 'rotom': '479', 'ditto': '132', 'dracozolt': '880', 'arctozolt': '881', 'dracovish': '882', 'arctovish': '883', 'charmander': '004', 'charmeleon': '005', 'charizard': '006', 'type: null': '772', 'silvally': '773', 'larvitar': '246', 'pupitar': '247', 'tyranitar': '248', 'deino': '633', 'zweilous': '634', 'hydreigon': '635', 'goomy': '704', 'sliggoo': '705', 'goodra': '706', 'jangmo-o': '782', 'hakamo-o': '783', 'kommo-o': '784', 'dreepy': '885', 'drakloak': '886', 'dragapult': '887', 'zacian': '888-c', 'zamazenta': '889-c', 'eternatus': '890',
           'bulbasaur': '001', 'ivysaur': '002', 'venusaur': '003', 'squirtle': '007', 'wartortle': '008', 'blastoise': '009', 'mewtwo': '150'}

RAID_STAR = ""
RAID_POKEMON = ""
RAID_OWNER = ""
OWNER_ID = {
    'sunny': 'SN',
    'kirbio': 'KB',
    'boomngong': 'BN',
    'bitah': 'BT'
}


def generateID(owner, total_posts):
    owner = owner.lower()
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
    embed.description = star
    # if raid['code'] != '':
    #     embed.description = '{}\n\n`{:4d}`'.format(star, int(raid['#']))
    # else:
    #     embed.description = '{}'.format(star)
    embed.add_field(name='ID', value='{}'.format(raid['#']))
    embed.add_field(name='passcode', value='{}'.format(raid['code']))
    embed.set_thumbnail(
        url=getThumbnailURL(raid['pokemon'], raid['gmax']))
    # url='img/ditto.png')
    embed.thumbnail.width = 64
    embed.thumbnail.height = 64
    # embed.set_author(name=raid['owner'])

    return embed


def embedRaidList(raids):
    embeds = []
    for raid in raids:
        embeds.append(embedRaid(raid))
    return embeds


async def setRaidStatusMessage(client, raidname):
    if raidname == "":
        await client.change_presence(status=None, activity=None)
        return

    # Until discord supports assets for Game type or enable fully custom status
    # This will offer more raids detail
    # raid_info = {"small_image":getThumbnailURL('toxtricity'),
    #             "small_text":raidname}

    # apparently the api does not support custom status yet :c
    game = discord.Game(name=raidname)
    await client.change_presence(status=discord.Status.dnd, activity=game)


def isAdminMessage(message):
    poster = message.author.name
    return poster == 'Kirbio' or poster == 'Sunny'


def getClosestMatch(name):
    # return closest match
    key = name.lower()
    if key in dexlist:
        return key

    match = get_close_matches(key, dexlist.keys(), n=1, cutoff=0.6)

    # if no match, use the original name
    if len(match) == 0:
        return key

    return match[0]

    # def getNatDexNo(name):
#     key = name.lower()
#     if key not in dexlist:
#         return "132"  # Ditto, for catch-all error
#     else:
#         return dexlist[key]


def getThumbnailURL(name, gmax=False):
    name = name.lower()

    if not name in dexlist:
        name = 'ditto'

    # special case
    # if name == 'toxtricity':
    #     name = 'toxtricity-amped'
    # elif name == 'meowstic':
    #     name = 'meowstic-male'

    if gmax:
        name += '-gmax'

    return 'https://play.pokemonshowdown.com/sprites/gen5/{}.png'.format(name)
