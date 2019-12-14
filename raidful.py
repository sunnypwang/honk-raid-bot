# importing the requests library 
import requests
import const
import util
  
# api-endpoint 
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {} 
  
# sending get request and saving the response as response object 

def getData():
    r = requests.get(url = const.SHEET_URL, params = PARAMS)
    data = r.json()
    return data

# extracting data in json format 
# data = getData()

def formatPokemon(data):
    isgmax = ""
    if(data['gmax']):
        isgmax = "G-"
    return str(data['rarity'])+" Star  "+isgmax+data['name']

def getUserPokemonList(owner):
    data = getData()
    result = []
    for i in data['items']:
        if i['owner']==owner:
            result.append(i)
    return result

def getAllPokemonList():
    data = getData()
    return data['items']

def getRaidbyID(id):
    r = requests.get(url = const.SHEET_URL + '/' + id)
    data = r.json()
    return data

# -------------
#  POST REQUEST
# -------------

def postRaid(params, owner):
    raid_data = {
        '#': util.generateID(owner, len(getUserPokemonList(owner))),
        'name': params[0],
        'rarity': 5,
        'gmax': False,
        'owner': owner,
        'opened': False
    }
    if 'G' in params:
        raid_data['gmax'] = True

    rarity = [num for num in [1,2,3,4] if str(num) in params] # [1] if params has '1'
    if rarity:
        raid_data['rarity'] = rarity[0]

    r = requests.post(url = const.SHEET_URL, json = raid_data)
    if r.status_code == requests.codes.ok:
        return formatPokemon(raid_data)
    else:
        return r.status_code + ' Cannot post the raid'

def startRaid(params):
    id = params[0]
    code = params[1] if len(params) > 1 else ''
    data = getRaidbyID(id)

    if 'error' in data.keys():
        return None

    data['opened'] = True
    data['code'] = code
    put_url = f'{const.SHEET_URL}/{id}&method=PUT'
    r = requests.post(url = put_url, json = data)
    return data
