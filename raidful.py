# importing the requests library
import requests
import const
import util
# api-endpoint

# defining a params dict for the parameters to be sent to the API
PARAMS = {}

# sending get request and saving the response as response object


def getData():
    r = requests.get(url=const.SHEET_URL, params=PARAMS)
    data = r.json()
    return data


def getAllRaid():
    data = getData()
    return data['items']


def getAllRaidbyOwner(owner):
    raids = getAllRaid()
    result = []
    for raid in raids:
        if raid['owner'] == owner:
            result.append(raid)
    return result


def getRaidbyID(id):
    r = requests.get(url=const.SHEET_URL + '/' + id.upper())
    print(r.url)
    data = r.json()
    return data


def getAllActiveRaid():
    active_raid = []
    raids = getAllRaid()
    for raid in raids:
        if raid['opened']:
            active_raid.append(raid)
    return active_raid


def listRaid(params):
    # list all raid
    if len(params) == 0:
        raids = getAllRaid()

    # list all raid for specified owner
    else:
        owner = params[0]
        raids = getAllRaidbyOwner(owner)
    print(raids)
    return util.embedRaidList(raids) if len(raids) > 0 else None

# -------------
#  POST REQUEST
# -------------


def postRaid(params, owner):

    if len(params) == 0:
        return 'Please provide Pokemon name (If Gigantamax please include G or GMax)'

    pokemon = params[0]
    rarity = 5
    gmax = False
    for param in params:
        if param.isdigit() and int(param) in [1, 2, 3, 4, 5]:
            rarity = int(param)
        if param in ['g', 'gmax', 'g-max']:
            gmax = True

    raid = {
        '#': util.generateID(owner, len(getAllRaidbyOwner(owner))),
        'pokemon': pokemon,
        'rarity': rarity,
        'gmax': gmax,
        'owner': owner,
        'opened': False,
        'code': '-'
    }

    r = requests.post(url=const.SHEET_URL, json=raid)
    if r.status_code == requests.codes.ok:
        return {'status': 'ok', 'msg': util.formatPokemon(raid) + '\nID: ' + raid['#']}
    else:
        return {'status': 'error', 'msg': 'Cannot post the raid'}


def openRaid(params, raid_start, owner):

    # raids = getAllRaidbyOwner(owner)
    # id = None
    # # if ID not specified but there are many raids
    # if len(params) < 1 and len(raids) > 1:
    #     return {'status': 'error', 'msg': 'Please provide raid ID (and optionally 4-digit passcode)'}
    # # if ID not specified but there is only single raid
    # elif len(params) < 1 and len(raids) == 1:
    #     id = raids[0]['#']
    # # if ID specified
    # elif len(params) > 1:

    # else:

    # OLD CODE BELOW

    if len(params) < 1:
        return {'status': 'error', 'msg': 'Please provide raid ID (and optionally 4-digit passcode)'}

    if raid_start:
        return {'status': 'error', 'msg': 'Another Raid is active!'}

    id = params[0].upper()
    code = '-'

    if len(params) > 1:
        code = params[1]
        if not code.isdigit() or len(code) != 4:
            return {'status': 'error', 'msg': 'Passcode must be 4-digit'}

    raid = getRaidbyID(id)

    if 'error' in raid.keys():
        return {'status': 'error', 'msg': 'ID not found. Please type `!list` for all available raids'}

    raid['opened'] = True
    raid['code'] = code
    put_url = f'{const.SHEET_URL}/{id}&method=PUT'
    r = requests.post(url=put_url, json=raid)

    return {'status': 'ok', 'embed': util.embedRaid(raid)}


def closeRaid():

    # In reality there should be only one active raid at a time
    raids = getAllActiveRaid()
    if not raids:
        return 'No active raid!'

    for raid in raids:
        raid['opened'] = False
        id = raid['#']
        put_url = f'{const.SHEET_URL}/{id}&method=PUT'
        r = requests.post(url=put_url, json=raid)

    return 'Raid closed!'


# -------------
#  DELETE REQUEST
# -------------


def deleteRaidbyID(id):
    put_url = f'{const.SHEET_URL}/{id}&method=DELETE'
    r = requests.post(url=put_url)


def deleteRaid(params, owner):
    if len(params) > 0:
        id = params[0]
        raid = getRaidbyID(id)
        if not raid:
            return 'ID not found!'
        if raid['owner'] == owner:
            deleteRaidbyID(id)
            return util.formatPokemon(raid) + ' deleted!'
        else:
            return 'This raid belongs to another trainer!'
        return 'Cannot delete raid! Please try again'
    else:
        raids = getAllRaidbyOwner(owner)
        for raid in raids:
            deleteRaidbyID(raid['#'])
        return 'All of your raids deleted!'


def deleteAllRaid():
    raids = getAllRaid()
    for raid in raids:
        id = raid['#']
        deleteRaidbyID(id)
    return 'All raids deleted!'
