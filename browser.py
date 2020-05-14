# write your code here

import sys
import os
import _collections
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init

init(autoreset=True)

if len(sys.argv) != 2:
    exit()

dir_name = sys.argv[1]

def make_directory(file_name, content):
    file_name = file_name.replace('.com', '').replace('https://', '').replace('www.', '')
    try:
        os.mkdir(dir_name)
    except:
        pass
    try:
        os.chdir(dir_name)
    except:
        pass
    try:
        with open('{}.txt'.format(file_name), 'w') as f:
            for c in content:
                f.write(c)
    except:
        print("Can't save the web page!")
    finally:
        os.chdir('..')

def send_request(web_site):
    r = requests.get(web_site)
    soups = BeautifulSoup(r.content, 'html.parser')
    list_parse = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'li', 'ul', 'ol']
    soups = soups.find_all(list_parse)
    return_string = ''
    for soup in soups:
        if soup.name == 'a':
            return_string += Fore.BLUE + soup.text + Fore.WHITE
            continue
        if soup.text == '\n' or soup.text == '':
            continue
        return_string += soup.text
    return return_string

visited = _collections.deque()

def check_web(web_site):
    if '.' in web_site and 'https://' in web_site:
        response = send_request(web_site)
        print(response)
        make_directory(web_site, response)
        visited.append(web_site)
    else:
        saved(web_site)
        visited.append(web_site)

def saved(web_s):
    try:
        os.chdir(dir_name)
        with open('{}.txt'.format(web_s), 'r') as f:
            print(f.readline())
    except:
        print('Error')
    finally:
        os.chdir('..')
        visited.append(web_s)

while True:
    web_sites = input()
    if web_sites == 'back' and len(visited) > 0:
        check_web(visited.popleft())
    else:
        if web_sites == 'back':
            print('No Visited websites found!')
        if 'https://' not in web_sites.lower() and '.' in web_sites:
            web_sites = 'https://' + web_sites
            check_web(web_sites)
        if 'https://' in web_sites:
            check_web(web_sites)
        elif web_sites == 'exit':
            sys.exit()
        
        else:
            saved(web_sites)



