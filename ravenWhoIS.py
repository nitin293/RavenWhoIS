import requests
import subprocess
import re
import os
import argparse


def banner():
    ban = '''
╭━━━╮╱╱╱╱╱╱╱╱╱╱╱╭╮╭╮╭┳╮╱╱╱╱╭━━┳━━━╮
┃╭━╮┃╱╱╱╱╱╱╱╱╱╱╱┃┃┃┃┃┃┃╱╱╱╱╰┫┣┫╭━╮┃
┃╰━╯┣━━┳╮╭┳━━┳━╮┃┃┃┃┃┃╰━┳━━╮┃┃┃╰━━╮
┃╭╮╭┫╭╮┃╰╯┃┃━┫╭╮┫╰╯╰╯┃╭╮┃╭╮┃┃┃╰━━╮┃
┃┃┃╰┫╭╮┣╮╭┫┃━┫┃┃┣╮╭╮╭┫┃┃┃╰╯┣┫┣┫╰━╯┃
╰╯╰━┻╯╰╯╰╯╰━━┻╯╰╯╰╯╰╯╰╯╰┻━━┻━━┻━━━╯

Author: Nitin Choudhury
Version: 0.1.0
    '''

    print(ban)


class WhoIS:

    def __init__(self, domain):
        self.domain = domain

    def getWhoIS_from_web(self):
        try:
            whois = {}

            whois_response = requests.get(f"https://lookup.icann.org/api/whois?q={self.domain}").json()
            whois_response = whois_response["records"][0]
            whois_response = whois_response["serverResponse"]["rawResponse"]
            whois_response = whois_response.split(">>>")[0].split('\n')[:-2]

            for obj in whois_response:
                key, value = obj.split(':')[0], ':'.join(obj.split(':')[1:])

                if key:
                    if key in whois and type(whois[key]) != list:
                        whois[key] = [whois[key]]
                        whois[key].append(value)
                    else:
                        whois[key] = value

            return whois

        except IndexError:
            return None


    def getWhoIS_from_pkg(self):
        try:
            whois = {}

            if os.name=="nt":
                whois_path = os.path.join("tools", "whois.exe")
                data = subprocess.check_output(f"{whois_path} {self.domain}", shell=True)
                data = re.findall(r"([Dd]omain [Nn]ame:.*)(?:>>>)", str(data))[0].split("\\r\\n")[:-2]

            elif os.name=="posix":
                data = subprocess.check_output(f"whois {self.domain}", shell=True)
                data = re.findall(r"([Dd]omain [Nn]ame:.*)(?:>>>)", str(data))[0].split("\\n")[:-2]

            else:
                raise os.error

            for obj in data:
                key, value = obj.split(":")[0], ':'.join(obj.split(":")[1:])
                if key:
                    if key in whois and type(whois[key]) != list:
                        whois[key] = [whois[key]]
                        whois[key].append(value)
                    else:
                        whois[key] = value

            return whois

        except:
            return None


def printWhoIS(DOMAIN):
    whois = WhoIS(DOMAIN)

    try:
        data = whois.getWhoIS_from_web()
    except:
        data = whois.getWhoIS_from_pkg()

    if data:
        for key in data.keys():

            if type(data[key]) in [list, set]:
                for obj in data[key]:
                    print(f"{key}:{obj}")

            else:
                print(f"{key}:{data[key]}")

    else:
        print(None)


if __name__ == '__main__':
    banner()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d", "--domain",
        help="Set Domain Name",
        required=True,
        type=str
    )

    args = parser.parse_args()

    domain = args.domain

    printWhoIS(domain)