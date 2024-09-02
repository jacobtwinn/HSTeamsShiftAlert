import requests
import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
HS_USERNAME = os.getenv("HS_USERNAME")
HS_PASSWORD = os.getenv("HS_PASSWORD")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

Client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def check_for_shifts():
   # Initializing webdriver

    options = webdriver.ChromeOptions()
    options.add_argument('window-position=0,0')
    options.page_load_strategy = 'normal'
    driver=webdriver.Chrome(options=options)

    ## Try catch to try to login to the HS website, then click the shift availible button to open shifts page
    
    try:
        
        driver.get("https://app.hotschedules.com/hs/login.jsp")
        username = driver.find_element(By.NAME,'username')
        password = driver.find_element(By.NAME,'password')
        username.send_keys(HS_USERNAME)
        password.send_keys(HS_PASSWORD)
        username.send_keys(Keys.RETURN)
      # Sometimes the continue button appears use in case
        try: 
            continue_button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.ID, "button1"))
            )
        #  Click the "Continue" button
            continue_button.click()
            print("Clicked the Continue button.")
            
        except: 
            print("Couldnt find continue button, proceeding...")
            ## Shift page click implementation
        time.sleep(3)
        
        try :
        
            shift_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.ID, "Available Pickup1"))
            )
            
            shift_button.click()
            print("Clicked the 'Shift' button.")
        except: 
            print("Could not find the Shift button, ")
            

        time.sleep(5)

        ## Parser html to look for shift class, if there it will know if there is open shift
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        shifts = soup.find_all('div', class_='shift-pickup-item')



        if shifts:
            print('Shift Found!')
            message = Client.messages.create(
    
            body = "Alert! There is a shift! Check HS App!",
            from_ = TWILIO_PHONE_NUMBER,
            to = RECIPIENT_PHONE_NUMBER
            )
            print(message.sid)
            driver.quit()
            exit()
        else:
            print('Shift Not Found!')
    finally:
        driver.quit()
        print("Window Closed")

while True:
    timer = random.randint(60,85)
    print(timer)
    check_for_shifts()
    time.sleep(timer)
