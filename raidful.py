# importing the requests library 
import requests
import tokens_const
  
# api-endpoint 
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {} 
  
# sending get request and saving the response as response object 

def getData():
    r = requests.get(url = os.environ['SHEET_URL'], params = PARAMS)
    data = r.json()
    return data

# extracting data in json format 
data = getData()

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


