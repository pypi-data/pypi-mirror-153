import shlex
import argparse
import os
from subprocess import Popen, PIPE
from ._discord import Discord

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--install", required=False, help="Use this parameter to install all Discord clients.")
    args = vars(ap.parse_args())
    if args["install"] not in ["stable", "ptb", "canary", "development", "all", None]:
        print(
            f"{args['install']} is not a valid version, please use one of the following: \"stable\", \"ptb\", \"canary\", \"development\" or \"all\"")
        exit()

    discord = Discord()

    clientsToReinstall = {
        "stable": False,
        "ptb": False,
        "canary": False,
        "development": False
    }

    if not os.path.exists("/usr/share/discordup/installed"):
        print("\033[1m" + "SETUP" + ":\033[0m", "Running first time setup ...")
        input("\033[1m" + "SETUP" + ":\033[0m Please close all instances of Discord and then click enter")
        print("\033[1m" + "SETUP" + ":\033[0m", "This may take a few seconds please be patient, your Discord application may disapeer, don't worry it will come back")
        clientsToReinstall = discord.setup()
        for command in ["sudo mkdir /usr/share/discordup", "sudo touch /usr/share/discordup/installed"]:
            _command = shlex.split(command)
            process = Popen(_command, stdout=PIPE, stderr=PIPE)
            process.communicate()

    installations = discord.findInstallations()
    if args["install"] == "all":
        for installation in installations:
            installations[installation]["installed"] = True
            installations[installation]["version"] = "-1"
    elif args["install"] != None:
        installations[args["install"]]["installed"] = True
        installations[args["install"]]["version"] = "-1"

    for key, value in clientsToReinstall.items():
        if value:
            installations[key]["installed"] = True
            installations[key]["version"] = "-1"

    for installation, details in installations.items():
        if details["installed"]:
            updateStatus = discord.update(installation, details["version"])
            print("\033[1m"+installation.upper()+":\033[0m", updateStatus)
        else:
            print("\033[1m"+installation.upper()+":\033[0m", "Not installed")

if __name__ == "__main__":
    main()