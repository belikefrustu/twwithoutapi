from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random


class TwitterBot:
    def __init__(self, username, password):
        '''
        This method asign the username and the password parameters inputs in the driver that will be used in the following methods
        '''
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome(executable_path='C:/Users/Usuario/Desktop/Twitterbot/chromedriver.exe') # WARNING: Write your own path

    def login(self):
        '''
        In this method firstly the driver searchs the login page of twitter, then detects the user and the password boxes and clean
        and fill them with the established parameters
        '''
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(3)

        email = bot.find_element("xpath", '//input[@autocomplete="username"]')
        email.clear()
        email.send_keys(self.username)
        email.send_keys(Keys.RETURN)
        time.sleep(3)

        password = bot.find_element("xpath", '//input[@name="password"]')
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(3)

    def follow_from_user(self, user):
        '''
        This method firstly reject the cookies pop-up to avoid future click problems, then search the user inputed and his 
        "following page". After a quick scroll in that page detects all the usernames and store them in a list that will later be the
        index from wich follow each of them.

        The method also has a counter to control the number of follows and a random interval of seconds to make it in the most natural 
        way posible in order to avoid possible bans. This is fully explained in the github documentation.
        '''

        bot = self.bot

        RejectCookies = bot.find_element("xpath", '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]/div/span/span')        
        RejectCookies.click()
        
        bot.get("https://twitter.com/"+ user)
        time.sleep(3)
        bot.get("https://twitter.com/"+ user + "/followers")
        time.sleep(3)

        arrobas = bot.find_elements("xpath", '//a[@role="link" and @aria-hidden="true"]')
        lista_arrobas = [arroba.get_attribute('href') for arroba in arrobas]

        lista_arr_def = []
        for arroba in lista_arrobas:
            arroba = "@" + arroba.split("/")[3]
            lista_arr_def.append(arroba)
        
        print("Lista de @ detectados (", len(lista_arr_def), "): ", lista_arr_def)

        cont_follows = 0

        for n in lista_arr_def:
                   
            time.sleep(2)
            follows_b = bot.find_element(By.XPATH, "//div[@aria-label='Follow " + n + "']")
            webdriver.ActionChains(bot).move_to_element(follows_b).click(follows_b).perform()
            print("You have followed ", n)
            time.sleep(2)

            if cont_follows <= 4:
                cont_follows += 1
                print("You have " + str(cont_follows) + " consecutive follows, " 
                        + str(5 - cont_follows) + " left for the next break (20 min)")
                time.sleep(random.randint(6,30))


            if cont_follows > 4:
                print("You have 5 consecutive follows, its time to stop (20 min)")
                cont_follows = 0
                time.sleep(1200)
                
UserParameters = TwitterBot('Probando2847', 'Hello01134') # ('username', 'password')
UserParameters.login()
UserParameters.follow_from_user('Cristiano') # ('username')