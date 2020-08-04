from time import sleep
from selenium import webdriver
import colorama
import requests
import pyfiglet
import os
from colorama import init, Fore, Back, Style
init(convert=True)

ascii_banner = pyfiglet.figlet_format("NameMC Friender")
os.system("cls")
print(Fore.GREEN + ascii_banner)
print(Fore.GREEN + 'v1.1 SNAPSHOT by ' + Fore.CYAN + 'https://github.com/Diszyyy')
print("")

email_address = str(input(Fore.CYAN + "Email address: " + Fore.WHITE))
password = str(input(Fore.CYAN + "Password (it's hidden): " + Fore.BLACK))
username = str(input(Fore.CYAN + "Copy all friends from: " + Fore.WHITE))

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
options.add_argument("--log-level=OFF")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.set_window_size(300, 600)
driver.get("https://namemc.com/login")
sleep(3)

def tryLogin():
    try:
        email = driver.find_element_by_id("email").send_keys(str(email_address))
    except:
        print(Fore.RED + "NameMC login page hasn\'t been loaded yet. Retrying in 3 seconds.")
        sleep(3)
        tryLogin()
tryLogin()
	
sleep(0.3)

driver.find_element_by_id("password").send_keys(str(password))
sleep(0.5)

driver.find_element_by_xpath("/html/body/main/div/div/div/div/div[2]/form/div/button").click()
sleep(1)


def checkLogin():
    try:
        loggedName = driver.find_element_by_xpath('//a[@class="nav-link dropdown-toggle text-nowrap pl-0"]/span').text
        return loggedName
    except:
        print(Fore.RED + "Wrong credentials. Closing program!")
        exit()
checkLogin()

driver.get("https://namemc.com/profile/" + str(username))

def getUUID():
    try:
        uuid = driver.find_element_by_xpath('//div[@class="col-12   order-md-2 col-md"]/samp').text
        return uuid
    except:
        print(Fore.RED + "Couldn\'t fetch UUID of " + str(username))
        getUUID()

uuid = getUUID()
loggedName = checkLogin()
r = requests.get("https://api.namemc.com/profile/" + uuid + "/friends")
os.system("cls")
print(Fore.GREEN + ascii_banner)
print(Fore.GREEN + 'v1.1 SNAPSHOT by ' + Fore.CYAN + 'https://github.com/Diszyyy' + Fore.WHITE + ' - ' + Fore.GREEN + 'logged in as ' + Fore.YELLOW + loggedName)
print(Fore.GREEN + username + "'s UUID is: " + Fore.YELLOW + uuid)

events = r.json()
for event in events:
    try:
        driver.get("https://namemc.com/profile/" + event['name'])
        sleep(1)
        driver.find_element_by_css_selector('#add-friend-button').click()
        print(Fore.GREEN + "added " + Fore.CYAN + event['name'] + Fore.GREEN + " as friend." + Fore.RED)
        sleep(30)
    except:
        print(Fore.RED + "you already had " + Fore.CYAN + event['name'] + Fore.RED + " as friend." + Fore.RED)
        continue
