from gitreturn import bcolors
import os

upToDate = f"{bcolors.HEADER}😎 Your branch is up to date! Happy hacking!{bcolors.ENDC}"

def createdSuccess(branch):
    return f"{bcolors.HEADER}😎 {branch} was created successfully! Happy hacking!{bcolors.ENDC}"

def checkingOut(branch):
    f"{bcolors.OKGREEN}🔍 Checking out and pulling from {branch}...{bcolors.ENDC}"

def saving(branch):
    return f"{bcolors.OKGREEN}💾 Saving any unstaged changes from {branch}...{bcolors.ENDC}"

def beforeAfter(branch, direction):
    f"{bcolors.HEADER}✨ You are in the branch you made {direction} {branch}!{bcolors.ENDC}"
savedSuccess = f"{bcolors.HEADER}Saved files or last stash loaded.{bcolors.ENDC}"
getSaved = f"{bcolors.OKGREEN}🦮 Getting your saved files...{bcolors.ENDC}"
noSetup = f"{bcolors.FAIL}🚫 You must run `git_return setup` first.{bcolors.ENDC}"
def prevNext(direction):
    return f"{bcolors.WARNING}💭 No {direction} branch recorded.{bcolors.ENDC}"
noPrev = f"{bcolors.WARNING}💭 No previous branch recorded.{bcolors.ENDC}"
noBranch = "No branch name was provided."
noCard = "No card was selected."
stoppedEarly = "Script may have been stopped early. Try removing .gitreturn."
invalidName = "Fatal git error: Invalid branch name."
packageUpdate = f"{bcolors.HEADER}⏳ Bringing your packages up to date!{bcolors.ENDC}"
def getSetEnvString(var, varType):
    print(f"{bcolors.WARNING}💭 You need to set your Trello {varType} in the environment.{bcolors.ENDC}")
    if (os.name == "nt"):
        return f"{bcolors.WARNING}💭 You can do this by running the following command: setx {var} <{varType}>{bcolors.ENDC}"
    else:
        return f"{bcolors.WARNING}💭 You can do this by running the following command: export {var}=<{varType}>\n{bcolors.WARNING}You may additionally need to put this into your ~/.bashrc or ~/.zshrc file{bcolors.ENDC}"
noKeyHelp = f"{bcolors.HEADER}Don't have a key? Make one here: {bcolors.ENDC}https://trello.com/app-key{bcolors.HEADER} or request one from your organization.{bcolors.ENDC}"
def noTokenHelp(key):
    return f"{bcolors.HEADER}Don't have a token? Get one here {bcolors.ENDC}https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=Server Token&key={key}"

def trelloBranchCreate(url):
    return f"{bcolors.OKGREEN}🔍 Creating a new branch from {bcolors.ENDC}{url}{bcolors.OKGREEN}...{bcolors.ENDC}"
