from gitreturn import bcolors, strings
import requests
import json
from InquirerPy import inquirer
import sys
import os

def getAPIToken():
    return inquirer.text(
        message="Enter your Trello API token:",
    ).execute()

def getAPIKey():
    return inquirer.text(
        message="Enter your Trello API key:",
    ).execute()

# 💭 You need to set your Trello key in the environment.
# Don't have a key? Make one here: https://trello.com/app-key or request one from your organization.
# 💭 You can do this by adding exports to your terminal file like ~/.zshrc or ~/.bashrc:
# ? Enter your Trello API token: 

def evaluateEnv(key, varType):

    try:
        var = os.environ.get(key)
        if not var:
            raise Exception(f"{key} not set")
    except:
        print(strings.setEnv(varType))
        print(strings.noKeyHelp if varType == "key" else strings.noTokenHelp(os.environ.get("GITRETURN_TRELLO_KEY")))
        if (os.name == "nt"):
            print(strings.setx(key, f"<{varType}>"))
        else:
            print(strings.export)
            print(strings.envExportCommand(key, getAPIKey() if varType == "key" else getAPIToken()))

        sys.exit(1)

baseUrl = "https://api.trello.com/1/"

headers = {
   "Accept": "application/json"
}

def get(url):
    query = {
       'key': os.environ.get("GITRETURN_TRELLO_KEY"),
       'token': os.environ.get("GITRETURN_TRELLO_TOKEN"),
    }

    return requests.get(baseUrl + url, params=query, headers=headers)

def getCards():
    user = get('members/me').json()
    res = get(f"members/{user['id']}/cards")
    return json.loads((res.text))

def parseCards():
    cards = getCards()
    return [{'name': card['name'], 'url': card['url']} for card in cards]

def pickCard():
    cards = parseCards()

    cardNames = [card['name'] for card in cards]
    cardUrls = {card['name']: card['url'] for card in cards}

    card = inquirer.fuzzy(
        message="Select a card:",
        choices=cardNames,
        max_height="50%",
    ).execute()

    print(f"{bcolors.HEADER}{card}{bcolors.ENDC}")
    print(cardUrls[card])

    if inquirer.confirm(
        message="Do you want to make a branch based on this card?",
    ).execute():
        return cardUrls[card]

    if not inquirer.confirm(
        message="Do you want to quit?",
    ).execute():
        return pickCard()

    return None
