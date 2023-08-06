from InquirerPy import inquirer
from gitreturn import trello, strings, git, exceptions
from os.path import exists
import json
import os
import sys
import re

def getCommitType(commitizen):
    if not commitizen:
        return ""

    commit = inquirer.fuzzy(
            message="What type of commit is this?",
            choices=[
                "feat",
                "fix",
                "docs",
                "style",
                "refactor",
                "perf",
                "test",
                "chore",
                "revert",
                "WIP",
            ],
        ).execute()

    return f"{commit}/"

def parseUrl(url):
    if url:
        formattedUrl = re.search(r'(?<=\/c\/\w{8}\/).{0,25}(?=-)', url)
        if formattedUrl:
            return formattedUrl.group(0)

    return None

def getNameTrello(commitizen):
    url = trello.pickCard()

    if url:
        commitType = getCommitType(commitizen)

        print(strings.trelloBranchCreate(url))

        if not parseUrl(url):
            raise exceptions.noBranch

        return f"{commitType}{parseUrl(url)}"

    raise exceptions.noCard

def getName(commitizen):
    commit = getCommitType(commitizen)

    branch = inquirer.text(
        message="What is the name of the branch?",
    ).execute()

    if not branch:
        raise exceptions.noBranch

    return f"{commit}{branch}"

def setup():
    remote = None
    default = None

    setup = inquirer.select(
        message="What do you want to do?",
        choices=[
            "Setup a remote",
            "Setup a default branch",
        ],
    ).execute()

    if setup == "Setup a remote":
        remote = inquirer.text(
            message="What is the remote name?",
            default="origin",
        ).execute()

    if setup == "Setup a default branch":
        default = inquirer.text(
            message="What is the default branch name?",
            default="main",
        ).execute()

    pacman = inquirer.select(
            message="What package manager do you use?",
            choices=[
                "npm",
                "yarn",
            ],
        ).execute()

    trello = inquirer.confirm(
        message="Do you want to use Trello?",
    ).execute()

    commitizen = inquirer.confirm(
        message="Do you want to use commitizen-style branches?",
    ).execute()

    config = {
        "pacman": pacman,
        "trello": trello,
        "commitizen": commitizen,
    }

    if remote:
        config["remote"] = remote 
    else:
        config["default"] = default

    with open("config.json", "w") as f:
        json.dump(config, f)

    open(".gitreturn", "w").write(json.dumps(config))

def loadConfig():
    config = json.loads(open(".gitreturn").read())

    default = None
    trelloc = None
    commitizenc = None
    remotec = None
    defaultc = None

    if 'trello' in config:
        trelloc = config['trello']

    if 'commitizen' in config:
        commitizenc = config['commitizen']

    if 'remote' in config:
        remotec = config['remote']

    if 'default' in config:
        defaultc = config['default']

    pacman = config['pacman']

    if not remotec and not defaultc:
        raise exceptions.stoppedEarly

    default = git.getRemote(config['remote']) if remotec else config['default']

    return default, trelloc, commitizenc, pacman

def move(stash, direction, branch):
    beforeAfter = "after" if direction == "after" else "before"
    prevNext = "next" if direction == "after" else "previous"
    branchToMove = branch.after if direction == "after" else branch.before
    branchMovedFrom = branch.after if direction == "before" else branch.before

    if (direction and branchToMove != branch.curr):
        print(strings.getSaved)
        git.get(branchToMove)
        git.load(stash)
        print(strings.beforeAfter(branchMovedFrom, beforeAfter))
    else:
        print(strings.prevNext(prevNext))

def installPackages(pacman):
    if pacman == "npm":
        os.system("npm install")
    else:
        os.system("yarn")

def run():
    stash = "0"

    if len(sys.argv) == 2 and sys.argv[1] == "setup":
        setup()
        return

    if (not exists(".gitreturn")):
        print(strings.noSetup)
        sys.exit(1)

    default, trelloc, commitizenc, pacman = loadConfig()
    branch = git.Branch()

    list = git.getStashes()
    for line in list.split("\n"):
        if git.stashName in line:
            stash = list.split("\n").index(line)
            break

    if "--prev" in sys.argv or "-p" in sys.argv:
        move(stash, "before", branch)
    elif "--next" in sys.argv or "-n" in sys.argv:
        move(stash, "after", branch)
    elif "--load" in sys.argv or "-l" in sys.argv:
                print(strings.getSaved)
                git.load(git.stashName)
                print(strings.savedSuccess)
    else:
        if trelloc:
            trello.evaluateEnv("GITRETURN_TRELLO_KEY", "key")
            trello.evaluateEnv("GITRETURN_TRELLO_TOKEN", "token")

        if (branch.curr != default):
            print(strings.saving(branch.curr))
            git.save()
            print(strings.checkingOut(default))
            git.get(default)
            git.setLast(branch.curr)

        git.pull()
        print(strings.packageUpdate)
        installPackages(pacman)

        if inquirer.confirm(
                message="Do you want to create a new branch?",
            ).execute():

            if trelloc and not inquirer.confirm(
                    message="Do you want to use Trello?",
                ).execute():
                trelloc = False
            if trelloc:
                new = getNameTrello(commitizenc)
            else:
                new = getName(commitizenc)

            git.setNext(new)
            checkout = git.set(new)
            if checkout:
                checkout = checkout.read().decode("utf-8")
                if "is not a valid branch name" in checkout:
                    raise exceptions.invalidName
            git.setLast(branch.curr)
            print(strings.createdSuccess(new))
        else:
            print(strings.upToDate)

