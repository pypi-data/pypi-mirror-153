from gitreturn import bcolors

upToDate = f"{bcolors.HEADER}😎 Your branch is up to date! Happy hacking!{bcolors.ENDC}"

def createdSuccess(branch):
    print(f"{bcolors.HEADER}😎 {branch} was created successfully! Happy hacking!{bcolors.ENDC}")

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

def trelloBranchCreate(url):
    return f"{bcolors.OKGREEN}🔍 Creating a new branch from {bcolors.ENDC}{url}{bcolors.OKGREEN}...{bcolors.ENDC}"
