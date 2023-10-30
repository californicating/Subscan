#!/usr/bin/python3

import os
import platform
import requests
import time

class colors:
    fgRed = "\033[31m"
    fgGreen = "\033[32m"
    fgYellow = "\033[33m"
    fgBlue = "\033[34m"
    fgMagenta = "\033[35m"
    fgCyan = "\033[36m"
    fgWhite = "\033[37m"

try:
    from urllib3.util.url import parse_url
    from urllib.request import urlopen
    import argparse
    import urllib3
    import urllib

except ImportError or ModuleNotFoundError:
    question = input(colors.fgRed+"[Error: missing modules] Run setup file ? (y/n)")
    if question == "y":
        print(colors.fgGreen+"[!] Running setup.sh")
        os.system("bash setup.sh")
    elif question == "n":
        print(colors.fgRed+"[!] Exiting...")
        exit(0)

if platform.system() != "Linux":
    print(colors.fgRed+"[!] Sorry this tool is supported for Linux only")
    exit(0)
else:
    if os.geteuid() != 0:
        exit(colors.fgRed+"[!] Detected linux but you need root privileges to run this script.")

    def connection():
        try:
            urlopen('https://google.com', timeout=1)
            return True
        except urllib.error.URLError as Error:
            return False
    if connection():
        print(colors.fgBlue+"Connected to the internet " + colors.fgBlue+"[" + colors.fgGreen+'\u2713'+ colors.fgBlue+"]")
    else:
        print(colors.fgRed+"[!] Make sure you are connected to the internet . Exiting !")
        exit(0)

version = 2.0


def banner():
    os.system("clear")
    print("""
███████╗██╗   ██╗██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
██╔════╝██║   ██║██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
███████╗██║   ██║██████╔╝███████╗██║     ███████║██╔██╗ ██║
╚════██║██║   ██║██╔══██╗╚════██║██║     ██╔══██║██║╚██╗██║
███████║╚██████╔╝██████╔╝███████║╚██████╗██║  ██║██║ ╚████║
╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """)
    print(colors.fgRed+"Developed by @californicating")
    print(colors.fgGreen+"Version "+str(version))
    print("")

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', type=str, required=True, help=colors.fgMagenta+ 'Target Domain.')
    parser.add_argument('-o', '--output', type=str, required=False, help=colors.fgMagenta+'Output to file.')
    return parser.parse_args()

def parse_url(url):
    try:
        host = urllib3.util.url.parse_url(url).host
    except Exception as e:
        print('[*] Invalid domain , retry.')
        exit(0)
    return host

def write_subs_to_file(subdomain, output_file):
    with open(output_file, 'a') as fp:
        fp.write(subdomain + '\n')
        fp.close()

def main():
    banner()
    subdomains = []

    args = parse_args()
    target = parse_url(args.domain)
    output = args.output

    print(colors.fgBlue+"[!] Scanning "+str(target)+colors.fgRed+(" Please be patient task might take a while"))
    print("")
    print(colors.fgMagenta+"[!] Results : ")
    requesting = requests.get(f'https://crt.sh/?q=%.{target}&output=json')

    if requesting.status_code != 200:
        print('[+] Information not available or connection is slow , try again')
        exit(0)

    for (key,value) in enumerate(requesting.json()):
        subdomains.append(value['name_value'])

    subs = sorted(set(subdomains))

    counter = 1
    for s in subs:
        counter +=1
        print(colors.fgRed+"["+str(counter)+"]"+colors.fgBlue+f'{s}')
        if output is not None:
            write_subs_to_file(s, output)

    print(colors.fgGreen+"[!] Scan completed")

if __name__=='__main__':
    main()
