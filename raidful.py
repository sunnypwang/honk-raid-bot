# importing the requests library
import requests
import const
import util
# from tqdm import tqdm
# api-endpoint

# defining a params dict for the parameters to be sent to the API
PARAMS = {}

# sending get request and saving the response as response object

# local cache for faster access
LOCAL_RAIDS = []


# DEPRECATED
def getData():
    r = requests.get(url=const.SHEET_URL, params=PARAMS)
    data = r.json()
    return data


def getRaids(remote=False):
    global LOCAL_RAIDS

    if remote:           # if fetch from remote
        r = requests.get(url=const.SHEET_URL, params=PARAMS)
        # print('remote :', r.json()['items'])
        return r.json()['items']
    else:
        # print('local :', LOCAL_RAIDS)       # fetch from local
        return LOCAL_RAIDS


def updateLocal():
    global LOCAL_RAIDS
    r = requests.get(url=const.SHEET_URL, params=PARAMS)
    LOCAL_RAIDS = r.json()['items']
    print('Local Cache updated!')


def updateRemote():
    global LOCAL_RAIDS

    # Delete remote data and replace by local one
    remote_raids = getRaids(remote=True)

    print('Removing remote...')
    for raid in remote_raids:
        put_url = '{}/{}&method=DELETE'.format(const.SHEET_URL, raid['#'])
        r = requests.post(url=put_url)

    print('Copying to remote...')
    for raid in LOCAL_RAIDS:
        put_url = '{}/{}&method=PUT'.format(const.SHEET_URL, raid['#'])
        r = requests.post(url=put_url, json=raid)

    print('Database synced successfully!')
    return 'Database synced successfully!'


def logLocalRaids():
    global LOCAL_RAIDS
    print('Local Raid:')
    for raid in LOCAL_RAIDS:
        print(raid)


def getRaidbyID(id):
    # global LOCAL_RAIDS
    # if remote or not LOCAL_RAIDS:
    #     r = requests.get(url=const.SHEET_URL + '/' + id.upper())
    #     data = r.json()
    #     print(data)
    # else:
    # https://stackoverflow.com/a/8653568
    raids = getRaids()
    raid = next(
        (raid for raid in raids if raid['#'].upper() == id.upper()), None)
    return raid


def getRaidbyOwner(owner):
    # new code using mongoquery
    # not working for now
    # prevent URL injection maybe?
    # if ''' in owner:
    #    return []

    # r = requests.get(url=const.SHEET_URL, params={'owner',owner})
    # print(r.url)
    # data = r.json()

    # print(data)
    raids = getRaids()
    return [raid for raid in raids if raid['owner'].lower() == owner.lower()]


def getActiveRaids():
    raids = getRaids()
    return [raid for raid in raids if raid['opened']]


def listRaids(params):
    if len(params) > 0:
        raids = getRaidbyOwner(params[0])   # list all raids by owner
    else:
        raids = getRaids()                  # list all raids

    for raid in raids:
        print(raid)

    return util.embedRaidList(raids) if len(raids) > 0 else None

# -------------
#  POST REQUEST
# -------------


def postRaid(params, owner):
    global LOCAL_RAIDS
    owner = owner.lower()
    if len(params) == 0:
        return 'Please provide Pokemon name (If Gigantamax please include G or GMax)'

    pokemon = util.getClosestMatch(params[0])

    rarity = 5
    gmax = False
    for param in params:
        # if one param is a legit rarity specifier
        if param.isdigit() and int(param) in [1, 2, 3, 4, 5]:
            rarity = int(param)
        # if one param is legit gmax specifier
        if param in ['g', 'gmax', 'g-max']:
            gmax = True

    raid = {
        '#': util.generateID(owner, len(getRaidbyOwner(owner))),
        'pokemon': pokemon.lower(),
        'rarity': rarity,
        'gmax': gmax,
        'owner': owner.lower(),
        'opened': False,
        'code': '-'
    }

    LOCAL_RAIDS.append(raid)
    return util.formatPokemon(raid) + '\nID: ' + raid['#']

    # return 'Cannot post the raid'

    # r = requests.post(url=const.SHEET_URL, json=raid)
    # if r.status_code == requests.codes.ok:
    #     return {'status': 'ok', 'msg': util.formatPokemon(raid) + '\nID: ' + raid['#']}
    # else:
    #     return {'status': 'error', 'msg': 'Cannot post the raid'}


def openRaid(params, raid_start, owner):
    owner = owner.lower()
    raids = getRaidbyOwner(owner)  # get the raid list from the owner
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
    if not raid:
        return {'status': 'error', 'msg': 'ID not found. Please type `!list` for all available raids'}
    if raid['owner'] != owner:
        return {'status': 'error', 'msg': 'This raid belongs to another trainer!'}

    # dynamic binding
    raid['opened'] = True
    raid['code'] = code

    # put_url = f'{const.SHEET_URL}/{id}&method=PUT'
    # r = requests.post(url=put_url, json=raid)

    return {'status': 'ok', 'embed': util.embedRaid(raid), 'raid': raid}


def closeRaid():

    # In reality there should be only one active raid at a time
    raids = getActiveRaids()
    if not raids:
        return 'No active raid!'

    for raid in raids:
        raid['opened'] = False

    return 'Raid closed!'


# -------------
#  DELETE REQUEST
# -------------


def deleteRaidbyID(id):
    global LOCAL_RAIDS

    raid = getRaidbyID(id)
    LOCAL_RAIDS.remove(raid)


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
        raids = getRaidbyOwner(owner)
        for raid in raids:
            deleteRaidbyID(raid['#'])
        return 'All of your raids deleted!'


def deleteAllRaid():
    global LOCAL_RAIDS
    LOCAL_RAIDS.clear()
    return 'All raids deleted!'
