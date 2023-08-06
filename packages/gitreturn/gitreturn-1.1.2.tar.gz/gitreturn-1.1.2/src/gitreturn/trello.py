from gitreturn import bcolors
import requests
import json
from InquirerPy import inquirer
import sys
import os

def getSetEnvString(var, varType):
    print(f"{bcolors.WARNING}💭 You need to set your Trello {varType} in the environment.{bcolors.ENDC}")
    if (os.name == "nt"):
        return f"{bcolors.WARNING}💭 You can do this by running the following command: setx {var} <{varType}>{bcolors.ENDC}"
    else:
        return f"{bcolors.WARNING}💭 You can do this by running the following command: export {var}=<{varType}>\n{bcolors.WARNING}You may additionally need to put this into your ~/.bashrc or ~/.zshrc file{bcolors.ENDC}"

def setup():
    try:
        TRELLO_KEY = os.environ.get("GITRETURN_TRELLO_KEY")
        if not TRELLO_KEY:
            raise Exception("GITRETURN_TRELLO_KEY not set")
    except:
        print(getSetEnvString("GITRETURN_TRELLO_KEY", "key"))
        print(f"{bcolors.HEADER}Don't have a key? Make one here: {bcolors.ENDC}https://trello.com/app-key{bcolors.HEADER} or request one from your organization.{bcolors.ENDC}")

        sys.exit(1)

    try:
        TRELLO_TOKEN = os.environ.get("GITRETURN_TRELLO_TOKEN")
        if not TRELLO_TOKEN:
            raise Exception("GITRETURN_TRELLO_TOKEN not set")
    except:
        print(getSetEnvString("GITRETURN_TRELLO_TOKEN", "token"))
        print(f"{bcolors.HEADER}Don't have a token? Get one here {bcolors.ENDC}https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Server Token&key={TRELLO_KEY}")

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
