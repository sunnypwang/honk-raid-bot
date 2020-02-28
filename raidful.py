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
    # new code using mongoquery
    # not working for now
    # prevent URL injection maybe?
    # if '"' in owner:
    #    return []

    #r = requests.get(url=const.SHEET_URL, params={"owner",owner})
    # print(r.url)
    #data = r.json()

    # print(data)

    raids = getAllRaid()
    result = []
    for raid in raids:
        if raid['owner'] == owner:
            result.append(raid)

    return result


def getRaidbyID(id):
    r = requests.get(url=const.SHEET_URL + '/' + id.upper())
    # print(r.url)
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

    pokemon = util.getClosestMatch(params[0])

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

    raids = getAllRaidbyOwner(owner)  # get the raid list from the owner
    raid_id = None

    specified_id = True  # to keep track if the raid ID is specified or not

    # if the raid is already started
    if raid_start:
        return {'status': 'error', 'msg': 'Another Raid is active!'}

    # if the id is not specified
    if len(params) <= 1:
        if len(raids) > 1:
            # if no parameter are provided or the first one is passcode
            if len(params) == 0 or params[0].isdigit():
                return {'status': 'error', 'msg': 'Please provide raid ID (and optionally 4-digit passcode)'}
            else:
                raid_id = params[0].upper()
        elif len(raids) == 1:
            raid_id = raids[0]['#'].upper()
            specified_id = False
        else:
            return {'status': 'error', 'msg': 'You currently have no raid. Please add one first!'}
    else:
        raid_id = params[0].upper()

    code = '-'

    if len(params) > 1 or not specified_id:
        # check if any params has been provided or not
        if len(params) != 0:
            # if provided parmeter, check if it's correct or not
            if specified_id:
                code = params[1]

                # Check if the code is in correct format
                if not code.isdigit() or len(code) != 4:
                    return {'status': 'error', 'msg': 'Passcode must be 4-digit'}
            else:
                code = params[0]
                # Check if the code is in correct format.revert to none if it's not
                if not code.isdigit() or len(code) != 4:
                    code = '-'
                    raid_id = params[0]

    raid = getRaidbyID(raid_id)

    if 'error' in raid.keys():
        return {'status': 'error', 'msg': 'ID not found. Please type `!list` for all available raids'}

    if raid['owner'] != owner:
        return {'status': 'error', 'msg': 'This raid belongs to another trainer!'}

    raid['opened'] = True
    raid['code'] = code
    put_url = f'{const.SHEET_URL}/{id}&method=PUT'
    r = requests.post(url=put_url, json=raid)

    return {'status': 'ok', 'embed': util.embedRaid(raid), 'raid': raid}


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
    id = id.upper()
    put_url = f'{const.SHEET_URL}/{id}&method=DELETE'
    r = requests.post(url=put_url)


def deleteRaid(params, owner):
    owner = owner.lower()
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
