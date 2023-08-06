import PyInquirer as inquirer
from os.path import exists
import json
import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def setup():
    questions = [
        {
            'type': 'input',
            'name': 'remote',
            'message': 'What remote are you on?',
            'default': 'origin',
        },
        {
            'type': 'list',
            'name': 'pacman',
            'message': 'What package manager are you using?',
            'choices': [
                'npm',
                'yarn',
            ],
        }
    ]

    answers = inquirer.prompt(questions)

    answerMap = {}
    for answer in answers:
        answerMap[answer] = answers[answer]

    open(".gitreturn", "w").write(json.dumps(answers))

def run():
    if (not exists(".gitreturn")):
        setup()

    answers = json.loads(open(".gitreturn").read())
    default = os.popen(f"git remote show {answers['remote']} | sed -n '/HEAD branch/s/.*: //p'").read().strip()
    currentBranch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    lastBranch = os.popen('git config core.lastbranch').read().strip()
    nextBranch = os.popen('git config core.nextbranch').read().strip()

    if "--prev" in sys.argv or "-p" in sys.argv:
            if (lastBranch and lastBranch != currentBranch):
                print(f"{bcolors.OKGREEN}🦮 Getting your saved files...{bcolors.ENDC}")
                os.system(f"git checkout {lastBranch} &> /dev/null")
                os.system("git stash apply &> /dev/null")
                print(f"{bcolors.HEADER}✨ You are the branch you made before {currentBranch}!{bcolors.ENDC}")
            else:
                print(f"{bcolors.WARNING}💭 No previous branch recorded.{bcolors.ENDC}")
    elif "--next" in sys.argv or "-n" in sys.argv:
            if (nextBranch and nextBranch != currentBranch):
                print(f"{bcolors.OKGREEN}🦮 Getting your saved files...{bcolors.ENDC}")
                os.system(f"git checkout {nextBranch} &> /dev/null")
                os.system("git stash apply &> /dev/null")
                print(f"{bcolors.HEADER}✨ You are the branch you made after {currentBranch}!{bcolors.ENDC}")
            else:
                print(f"{bcolors.WARNING}💭 No next branch recorded.{bcolors.ENDC}")
    else:
        currentBranch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()

        print(f"{bcolors.OKGREEN}💾 Saving any unstaged changes from {currentBranch}...{bcolors.ENDC}")
        os.system(f"git stash save &> /dev/null")
        print(f"{bcolors.OKGREEN}🔍 Checking out and pulling from {default}...{bcolors.ENDC}")
        os.system(f"git checkout {default} &> /dev/null")
        os.system(f"git pull &> /dev/null")
        os.system(f"git config core.lastbranch {currentBranch}")

        print(f"{bcolors.HEADER}⏳ Bringing your packages up to date with {default}!{bcolors.ENDC}")
        if answers["pacman"] == "npm":
            os.system("npm install")
        else:
            os.system("yarn")

        questions = [
            {
                'type': 'confirm',
                'name': 'newBranch',
                'message': 'Do you want to create a new branch?',
            },
            {
                'type': 'input',
                'name': 'branchName',
                'message': 'What is the name of the branch?',
                'when': lambda answers: answers['newBranch']
            },
        ]

        answers = inquirer.prompt(questions)

        if answers["newBranch"]:
            os.system(f"git config core.nextbranch {answers['branchName']}")
            os.system(f"git checkout -b {answers['branchName']} &> /dev/null")
            os.system(f"git config core.lastbranch {currentBranch}")
            print(f"{bcolors.HEADER}😎 {answers['branchName']} was created successfully! Happy hacking!{bcolors.ENDC}")
        else:
            print(f"{bcolors.HEADER}😎 Your branch is up to date! Happy hacking!{bcolors.ENDC}")

