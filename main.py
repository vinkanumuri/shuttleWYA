from flask import Flask, request
#from jmespath import search
import requests
from twilio.twiml.messaging_response import MessagingResponse
import os
from twilio.rest import Client
# selenium scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

#account_sid = os.environ['TWILIO_ACCOUNT_SID'] 
account_sid = 'ACf8f2d3695691bb558c79f3beb0c60d76'
#auth_token = os.environ['TWILIO_AUTH_TOKEN']
auth_token = '05e6754fcacf46aee0b180c74efa62e2'
client = Client(account_sid, auth_token)

stops = {58381: ['784 memorial drive', 'mem drive', 'memorial drive', 'mem dr', 'memorial dr'], 
         5048: ['widener gate', 'widener'],
         5046: ['mather house', 'mather'], 
         5047: ['the inn', 'inn'],
         5043: ['maxwell dworkin', 'md'], 
         6248: ['science center', 'sc'],
         5044: ['memorial hall', 'mem hall', 'mem'], 
         5045: ['lamont library', 'lamont'],
         6854: ['leverett house', 'leverett', 'lev'], 
         5049: ['quad', 'quadrangle', 'radcliff quadrangle'],
         23509: ['radcliff yard'], 
         5050: ['mass and garden', 'mass ave', 'massachusetts ave', 'massachusetts avenue', 'yard', 'harvard yard'],
         5042: ['law school', 'law', 'harvard law'],
         5051: ['winthrop house', 'winthrop', 'throp'], 
         5036: ['1 western ave', 'western ave', 'western', 'western avenue'],
        #  5041: ['harvard square', 'square'], #northbound 
        #  58344: ['harvard square', 'square'], #southbound 
        #  5039: ['stadium'], #northbound
        #  23920: ['stadium'], #southbound
        #  5040: ['kennedy school', 'kennedy'], #northbound
        #  5054: ['kennedy school', 'kennedy'], #southbound
        #  58343: ['sec'], #sec 
        #  63189: ['sec', "barry's corner", 'barrys corner', 'barry corner'], #sec #northbound
        #  63190: ['sec', "barry's corner", 'barrys corner', 'barry corner'], #sec #southbound
        }

def scrapePassio(stop_name):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    DRIVER_PATH = '/Users/vinay/Dev/shuttleWYA/twilio-bot-venv/chromedriver'
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("https://shuttle.harvard.edu/")
    try:
        import time ###
        time.sleep(5)###
        driver.find_element(by=By.CLASS_NAME, value='form-control').send_keys(stop_name)
        time.sleep(5)###
        driver.find_element(by=By.CLASS_NAME, value='form-control').send_keys(Keys.RETURN)
        time.sleep(5)###
        info = driver.find_element(by=By.CLASS_NAME, value='infowindow').screenshot('screenshot.png')
    except NoSuchElementException:
        print('element not found')
    driver.quit()
    pass
    
app = Flask(__name__)
@app.route('/bot', methods=['GET', 'POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    # incoming_msg.lstrip(' ')
    # incoming_msg.rstrip(' ')
    responded = False

    for key in stops:
        if incoming_msg in stops[key]:
            # get relevant data from shuttle.harvard.edu
            stopid = str(key) ###
            msg = client.messages.create(to=request.values.get("From"), from_=request.values.get("To"),
                                         body=stopid) ###
            responded = True
            break

    if not responded:
        msg = client.messages.create(to=request.values.get("From"), from_=request.values.get("To"),
                                         body='Please text me a shuttle stop to get updates!')
    return '' #str(resp)

if __name__ == '__main__':
    #app.run()
    scrapePassio('widener')
     

    
