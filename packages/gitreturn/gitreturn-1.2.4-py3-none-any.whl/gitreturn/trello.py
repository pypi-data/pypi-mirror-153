from gitreturn import bcolors, strings
import requests
import json
from InquirerPy import inquirer
import sys
import os

def setup():
    try:
        TRELLO_KEY = os.environ.get("GITRETURN_TRELLO_KEY")
        if not TRELLO_KEY:
            raise Exception("GITRETURN_TRELLO_KEY not set")
    except:
        print(strings.getSetEnvString("GITRETURN_TRELLO_KEY", "key"))
        print(strings.noKeyHelp)

        sys.exit(1)

    try:
        TRELLO_TOKEN = os.environ.get("GITRETURN_TRELLO_TOKEN")
        if not TRELLO_TOKEN:
            raise Exception("GITRETURN_TRELLO_TOKEN not set")
    except:
        print(strings.getSetEnvString("GITRETURN_TRELLO_TOKEN", "token"))
        print(strings.noTokenHelp(TRELLO_KEY))

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
