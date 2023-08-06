from gitreturn import bcolors

def createdSuccess(branch):
    return f"{bcolors.HEADER}😎 {branch} was created successfully! Happy hacking!{bcolors.ENDC}"

def checkingOut(branch):
    return f"{bcolors.OKGREEN}🔍 Checking out and pulling from {branch}...{bcolors.ENDC}"

def saving(branch):
    return f"{bcolors.OKGREEN}💾 Saving any unstaged changes from {branch}...{bcolors.ENDC}"

def beforeAfter(branch, direction):
    return f"{bcolors.HEADER}✨ You are in the branch you made {direction} {branch}!{bcolors.ENDC}"

def prevNext(direction):
    return f"{bcolors.WARNING}💭 No {direction} branch recorded or you are already on the branch marked as {direction}.{bcolors.ENDC}"

def setEnv(varType):
    return f"{bcolors.WARNING}💭 You need to set your Trello {varType} in the environment.{bcolors.ENDC}"

def setx(var, varType):
    return f"{bcolors.WARNING}💭 You can do this by running the following command: setx {var} {varType}{bcolors.ENDC}"

def envExportCommand(var, varType):
    return f"{bcolors.OKCYAN}echo 'export {var}={varType}' >> ~/.zshrc # may need to change to ~/.bashrc\nsource ~/.zshrc{bcolors.ENDC}"

def noTokenHelp(key):
    return f"{bcolors.HEADER}Don't have a token? Get one here {bcolors.ENDC}https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&name=gitreturn&key={key}"

def trelloBranchCreate(url):
    return f"{bcolors.OKGREEN}🔍 Creating a new branch from {bcolors.ENDC}{url}{bcolors.OKGREEN}...{bcolors.ENDC}"

savedSuccess = f"{bcolors.HEADER}Saved files or last stash loaded.{bcolors.ENDC}"
getSaved = f"{bcolors.OKGREEN}🦮 Getting your saved files...{bcolors.ENDC}"
noSetup = f"{bcolors.FAIL}🚫 You must run `git_return setup` first.{bcolors.ENDC}"
noPrev = f"{bcolors.WARNING}💭 No previous branch recorded.{bcolors.ENDC}"
noBranch = "No branch name was provided."
noCard = "No card was selected."
stoppedEarly = "Script may have been stopped early. Try removing .gitreturn."
invalidName = "Fatal git error: Invalid branch name."
packageUpdate = f"{bcolors.HEADER}⏳ Bringing your packages up to date!{bcolors.ENDC}"
export = f"{bcolors.WARNING}💭 You can do this by adding exports to your terminal file like ~/.zshrc or ~/.bashrc:{bcolors.ENDC}"
upToDate = f"{bcolors.HEADER}😎 Your branch is up to date! Happy hacking!{bcolors.ENDC}"
noKeyHelp = f"{bcolors.HEADER}Don't have a key? Make one here: {bcolors.ENDC}https://trello.com/app-key{bcolors.HEADER} or request one from your organization.{bcolors.ENDC}"
