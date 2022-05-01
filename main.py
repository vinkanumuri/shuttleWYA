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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

account_sid = os.environ['TWILIO_ACCOUNT_SID'] 
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

stops = {'784 memorial drive': ['784 memorial drive', 'mem drive', 'memorial drive', 'mem dr', 'memorial dr'], #58381
         'widener gate': ['widener gate', 'widener'], #5048
         'mather house': ['mather house', 'mather'], #5046
         'the inn': ['the inn', 'inn'], #5047
         'maxwell dworkin': ['maxwell dworkin', 'md'], #5043
         'science center': ['science center', 'sc'], #6248
         'memorial hall': ['memorial hall', 'mem hall', 'mem'], #5044
         'lamont library': ['lamont library', 'lamont'], #5045
         'leverett house': ['leverett house', 'leverett', 'lev'], #6854
         'quad': ['quad', 'quadrangle', 'radcliff quadrangle'], #5049
         'radcliff yard': ['radcliff yard'], #23509
         'mass and garden': ['mass and garden', 'mass ave', 'massachusetts ave', 'massachusetts avenue', 'yard', 'harvard yard'], #5050
         'law school': ['law school', 'law', 'harvard law'], #5042
         'winthrop house': ['winthrop house', 'winthrop', 'throp'], #5051
         '1 western ave': ['1 western ave', 'western ave', 'western', 'western avenue'], #5036
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
        wait = WebDriverWait(driver, 10)
        #wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'form-control')))
        driver.find_element(by=By.CLASS_NAME, value='form-control').send_keys(stop_name)
        #wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'ui-menu ui-widget ui-widget-content ui-autocomplete ui-front')))
        time.sleep(5)###
        driver.find_element(by=By.CLASS_NAME, value='form-control').send_keys(Keys.RETURN)
        time.sleep(10)###
        #driver.get_screenshot_as_file('test.png')###
        #wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'infowindow'))) #cahnge to wait until load completely
        #wait.until(ec.visibility_of_element_located((By.CLASS_NAME, 'ui-menu ui-widget ui-widget-content ui-autocomplete ui-front')))
        info = driver.find_element(by=By.CLASS_NAME, value='infowindow')#
        info.screenshot('screenshot.png')
        print(info.get_attribute("innerHTML"))

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
            stop_name = str(key)
            scrapePassio(stop_name)
            print('check screenshot.png')
            '''msg = client.messages.create(to=request.values.get("From"), from_=request.values.get("To"),
                                         body='Shuttles arriving at '+stop_name, media_url='')'''
            responded = True
            break

    if not responded:
        msg = client.messages.create(to=request.values.get("From"), from_=request.values.get("To"),
                                         body='Please text me a shuttle stop to get updates!')
    return '' #str(resp)

if __name__ == '__main__':
    #app.run()
    scrapePassio('quad')

'''
TODO:
- get it to wait till loaded
- text back the correct details instead of taking screenshot
- if there's time change time delays to wait to loads
'''  

    
