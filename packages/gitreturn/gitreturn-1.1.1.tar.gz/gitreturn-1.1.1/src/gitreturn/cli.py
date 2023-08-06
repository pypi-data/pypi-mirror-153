import PyInquirer as inquirer
from gitreturn import trello, bcolors
from os.path import exists
import json
import os
import sys
import re
import subprocess

def getCommitType(commitizen):
    if not commitizen:
        return ""

    questions = [
        {
            'type': 'list',
            'name': 'type',
            'message': 'What type of commit is this?',
            'choices': [
                'feat',
                'fix',
                'chore',
                'docs',
                'style',
                'refactor',
                'perf',
                'test',
                'revert',
                'WIP',
            ],
        }
    ]

    answers = inquirer.prompt(questions)

    return f"{answers['type']}/"

def parseUrl(url):
    if url:
        formattedUrl = re.search(r'(?<=\/c\/\w{8}\/).{0,25}(?=-)', url)
        if formattedUrl:
            return formattedUrl.group(0)

    return None

def getBranchNameTrello(commitizen):
    questions = [
        {
            'type': 'confirm',
            'name': 'trello',
            'message': 'Do you want to create a new branch from a Trello issue?',
        },
    ]

    answers = inquirer.prompt(questions)

    if answers["trello"]:
        url = trello.pickCard()
        if url:
            commitType = getCommitType(commitizen)

            print(f"{bcolors.OKGREEN}🔍 Creating a new branch from {bcolors.ENDC}{url}{bcolors.OKGREEN}...{bcolors.ENDC}")

            if not parseUrl(url):
                raise Exception("No branch name was provided.")

            return f"{commitType}{parseUrl(url)}"

    return getBranchName(commitizen)

def getBranchName(commitizen):
    commitType = getCommitType(commitizen)
    questions = [
        {
            'type': 'input',
            'name': 'branchName',
            'message': 'What is the name of the new branch?',
        },
    ]

    answers = inquirer.prompt(questions)

    if not answers['branchName']:
        raise Exception("No branch name was provided.")

    return f"{commitType}{answers['branchName']}"

def setup():
    questions = [
        {
            'type': 'confirm',
            'name': 'remote',
            'message': 'Do you have a remote?',
        },
        {
            'type': 'input',
            'name': 'remote',
            'message': 'What remote are you on?',
            'default': 'origin',
            'when': lambda answers: answers['remote']
        },
        {
            'type': 'input',
            'name': 'default',
            'message': 'What is the name of the default branch?',
            'default': 'main',
            'when': lambda answers: not answers['remote']
        },
        {
            'type': 'list',
            'name': 'pacman',
            'message': 'What package manager are you using?',
            'choices': [
                'npm',
                'yarn',
            ],
        },
        {
            'type': 'confirm',
            'name': 'trello',
            'message': 'Do you want to use Trello?',
            'default': False,
        },
        {
            'type': 'confirm',
            'name': 'commitizen',
            'message': 'Do you want to use commitizen-style branches?',
            'default': False,
        },
    ]

    answers = inquirer.prompt(questions)

    answerMap = {}
    for answer in answers:
        answerMap[answer] = answers[answer]

    open(".gitreturn", "w").write(json.dumps(answers))

def run():
    # if git_return setup is called
    if len(sys.argv) == 2 and sys.argv[1] == "setup":
        setup()
        return

    if (not exists(".gitreturn")):
        print(f"{bcolors.FAIL}You must run `git_return setup` first.{bcolors.ENDC}")
        sys.exit(1)

    config = json.loads(open(".gitreturn").read())

    trelloAnswer = None
    commitizenAnswer = None
    remoteAnswer = None
    defaultAnswer = None
    default = None

    if 'trello' in config:
        trelloAnswer = config['trello']

    if 'commitizen' in config:
        commitizenAnswer = config['commitizen']

    if 'remote' in config:
        remoteAnswer = config['remote']

    if 'default' in config:
        defaultAnswer = config['default']

    questions = [
        {
            'type': 'confirm',
            'name': 'trello',
            'message': 'Do you want to use Trello?',
        },
    ]

    answers = inquirer.prompt(questions)

    if not answers['trello']:
        trelloAnswer = False

    if trelloAnswer:
        trello.setup()

    if not remoteAnswer and not defaultAnswer:
        raise Exception(f"Script may have been stopped early. Try removing .gitreturn.")

    if remoteAnswer:
        default = os.popen(f"git remote show {config['remote']} | sed -n '/HEAD branch/s/.*: //p'").read().strip()

    if defaultAnswer:
        default = config['default']

    currentBranch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    lastBranch = os.popen('git config core.lastbranch').read().strip()
    nextBranch = os.popen('git config core.nextbranch').read().strip()

    stash = "0"
    list = os.popen("git stash list").read()
    for line in list.split("\n"):
        if "Z2l0cmV0dXJuX3N0YXNo" in line:
            stash = list.split("\n").index(line)
            break

    if "--prev" in sys.argv or "-p" in sys.argv:
            if (lastBranch and lastBranch != currentBranch):
                print(f"{bcolors.OKGREEN}🦮 Getting your saved files...{bcolors.ENDC}")
                os.system(f"git checkout {lastBranch}")
                os.system(f"git stash apply stash@{{{stash}}}")
                print(f"{bcolors.HEADER}✨ You are in the branch you made before {currentBranch}!{bcolors.ENDC}")
            else:
                print(f"{bcolors.WARNING}💭 No previous branch recorded.{bcolors.ENDC}")
    elif "--next" in sys.argv or "-n" in sys.argv:
            if (nextBranch and nextBranch != currentBranch):
                print(f"{bcolors.OKGREEN}🦮 Getting your saved files...{bcolors.ENDC}")
                os.system(f"git checkout {nextBranch}")
                os.system(f"git stash apply stash@{{{stash}}}")
                print(f"{bcolors.HEADER}✨ You are in the branch you made after {currentBranch}!{bcolors.ENDC}")
            else:
                print(f"{bcolors.WARNING}💭 No next branch recorded.{bcolors.ENDC}")
    elif "--load" in sys.argv or "-l" in sys.argv:
                print(f"{bcolors.OKGREEN}🦮 Getting your saved files...{bcolors.ENDC}")
                os.system(f"git stash apply stash@{{{stash}}}")
                print(f"{bcolors.HEADER}Saved files or last stash loaded.{bcolors.ENDC}")
    else:
        currentBranch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()

        print(f"{bcolors.OKGREEN}💾 Saving any unstaged changes from {currentBranch}...{bcolors.ENDC}")
        os.system(f"git stash push -m 'Z2l0cmV0dXJuX3N0YXNo'")
        print(f"{bcolors.OKGREEN}🔍 Checking out and pulling from {default}...{bcolors.ENDC}")
        os.system(f"git checkout {default}")
        os.system(f"git pull")
        os.system(f"git config core.lastbranch {currentBranch}")

        print(f"{bcolors.HEADER}⏳ Bringing your packages up to date with {default}!{bcolors.ENDC}")
        if config["pacman"] == "npm":
            os.system("npm install")
        else:
            os.system("yarn")

        questions = [
            {
                'type': 'confirm',
                'name': 'newBranch',
                'message': 'Do you want to create a new branch?',
            },
        ]

        answers = inquirer.prompt(questions)

        if answers["newBranch"]:
            if trelloAnswer:
                branchName = getBranchNameTrello(commitizenAnswer)
            else:
                branchName = getBranchName(commitizenAnswer)

            os.system(f"git config core.nextbranch {branchName}")
            checkout = subprocess.Popen(f"git checkout -b {branchName}", stderr=subprocess.PIPE, shell=True).stderr
            if checkout:
                checkout = checkout.read().decode("utf-8")
                if "is not a valid branch name" in checkout:
                    raise Exception("Fatal git error: Invalid branch name.")
            os.system(f"git config core.lastbranch {currentBranch}")
            print(f"{bcolors.HEADER}😎 {branchName} was created successfully! Happy hacking!{bcolors.ENDC}")
        else:
            print(f"{bcolors.HEADER}😎 Your branch is up to date! Happy hacking!{bcolors.ENDC}")

