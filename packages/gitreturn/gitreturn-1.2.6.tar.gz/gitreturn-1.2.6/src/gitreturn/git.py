import os
import subprocess

stashName = "Z2l0cmV0dXJuX3N0YXNo"

def set(branch):
    return subprocess.Popen(f"git checkout -b {branch}", stderr=subprocess.PIPE, shell=True).stderr

def get(branch):
    os.system(f"git checkout {branch}")

def save():
    os.system(f"git stash push -m 'Z2l0cmV0dXJuX3N0YXNo'")

def load(stash):
    os.system(f"git stash apply stash@{{{stash}}} &> /dev/null")

def getStashes():
    return os.popen("git stash list").read()

def getRemote(remote):
    return os.popen(f"git remote show {remote} | sed -n '/HEAD branch/s/.*: //p'").read().strip()

def pull():
    os.system("git pull")

def getCurrent():
    return os.popen("git rev-parse --abbrev-ref HEAD").read().strip()

def setLast(branch):
    os.system(f"git config core.lastbranch {branch}")

def getLast():
    return os.popen('git config core.lastbranch').read().strip()

def setNext(branch):
    os.system(f"git config core.nextbranch {branch}")

def getNext():
    return os.popen('git config core.nextbranch').read().strip()

class Branch:
    curr = getCurrent()
    before = getLast()
    after = getNext()

