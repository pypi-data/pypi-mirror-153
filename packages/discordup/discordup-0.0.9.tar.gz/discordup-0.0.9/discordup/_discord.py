import shlex
import requests
import os
import tarfile
import json
import tempfile
from subprocess import Popen, PIPE
from ._distro import findDistroType

discordDictionary = {
    "stable": {
        "link": "https://discord.com/api/download?platform=linux&format=tar.gz",
        "name": "discord",
        "zipName": "Discord",
    },
    "ptb":{
        "link": "https://discord.com/api/download/ptb?platform=linux&format=tar.gz",
        "name": "discord-ptb",
        "zipName": "DiscordPTB",
    },
    "canary":{
        "link": "https://discord.com/api/download/canary?platform=linux&format=tar.gz",
        "name": "discord-canary",
        "zipName": "DiscordCanary",
    },
    "development":{
        "link": "https://discord.com/api/download/development?platform=linux&format=tar.gz",
        "name": "discord-development",
        "zipName": "DiscordDevelopment",
    },
}

class Discord:
    def __init__(self):
        self.distroType = findDistroType()

    def update(self, type, version):
        if type not in discordDictionary:
            raise SystemExit('Cannot find type in the link dictionary')
        resp = requests.get(discordDictionary[type]["link"])
        latestVersion = resp.url.split("/")[5]
        if latestVersion != version:
            completeName = os.path.join(tempfile.gettempdir(), resp.url.split("/")[-1])

            if os.path.exists(completeName):
                os.remove(completeName)

            with open(completeName, "wb") as f:
                f.write(resp.content)

            file = tarfile.open(completeName)
            folderLocation = completeName.replace(".tar.gz", "")
            file.extractall(folderLocation)
            file.close()

            os.rename(f"{folderLocation}/{discordDictionary[type]['zipName']}/discord.png", f"{folderLocation}/{discordDictionary[type]['zipName']}/{discordDictionary[type]['name']}.png")
            os.rename(f"{folderLocation}/{discordDictionary[type]['zipName']}", f"{folderLocation}/{discordDictionary[type]['name']}")

            command = shlex.split(f"sudo mv '{folderLocation}/{discordDictionary[type]['name']}/{discordDictionary[type]['name']}.png' '/usr/share/pixmaps'")
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            process.communicate()

            command = shlex.split(f"sudo mv '{folderLocation}/{discordDictionary[type]['name']}/{discordDictionary[type]['name']}.desktop' '/usr/share/applications/'")
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            process.communicate()

            command = shlex.split(f"sudo mv '{folderLocation}/{discordDictionary[type]['name']}' '/usr/share/'")
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            process.communicate()

            command = shlex.split(f"sudo rm -rf '{folderLocation}'")
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            process.communicate()

            os.remove(completeName)
            return "Has just been updated"
        return "Already up to date"

    def findInstallations(self): ################### Du skal lave en som sletter deb/flatpak versionerne første gang man kører med "sudo remove discord..." og sletter nuværende discord når den skal opdaterer, lav en mappe og fil som siger at discordup er installeret i /usr/share/discordup/installed.txt
        installations = {
            "stable":       {"installed": False, "version": -1},
            "ptb":          {"installed": False, "version": -1},
            "canary":       {"installed": False, "version": -1},
            "development":  {"installed": False, "version": -1}
        }

        for discordType in discordDictionary:
            try:
                installationVersion = json.load(open(f'/usr/share/{discordDictionary[discordType]["name"].replace("stable", "discord")}/resources/build_info.json'))["version"]
                installations[discordType]["installed"] = True
                installations[discordType]["version"] = installationVersion
            except Exception:
                pass

        return installations

    def setup(self):
        uninstalled = {
            "stable":       False,
            "ptb":          False,
            "canary":       False,
            "development":  False
        }

        if self.distroType == "debian":
            for discordType in discordDictionary:
                try:
                    command = shlex.split(f"sudo apt remove {discordDictionary[discordType]['name']} -y")
                    process = Popen(command, stdout=PIPE, stderr=PIPE)
                    process.communicate()

                    uninstalled[discordType] = True
                except Exception:
                    pass

        for flatpakCommand in ["flatpak uninstall com.discordapp.Discord -y", "flatpak uninstall com.discordapp.DiscordCanary -y"]:
            try:
                command = shlex.split(flatpakCommand)
                process = Popen(command, stdout=PIPE, stderr=PIPE)
                process.communicate()

                if flatpakCommand == "flatpak uninstall com.discordapp.Discord -y":
                    uninstalled["stable"] = True
                elif flatpakCommand == "flatpak uninstall com.discordapp.DiscordCanary -y":
                    uninstalled["canary"] = True
            except Exception:
                pass

        return uninstalled

if __name__ == "__main__":
    self = Discord()
    self.setup("stable")