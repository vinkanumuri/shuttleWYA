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
    #options.headless = True
    options.add_argument("--window-size=1920,1200")
    DRIVER_PATH = '/Users/vinay/Dev/shuttleWYA/twilio-bot-venv/chromedriver'
    driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get("https://shuttle.harvard.edu/")
    try:
        import time
        time.sleep(3)
        driver.find_element(by=By.CLASS_NAME, value='form-control').send_keys(stop_name)
        time.sleep(2)
        driver.find_element(by=By.CLASS_NAME, value='form-control').send_keys(Keys.RETURN)
        time.sleep(4)
        info = driver.find_element(by=By.CLASS_NAME, value='infowindow')#
        info.screenshot('screenshot.png')
        infohtml = info.get_attribute("innerHTML")
        ### create dictionary of details
        import re
        infohtml = infohtml.replace('<i class="glyphicon glyphicon-heart"></i>', "a")
        try:
            shuttle_names = []
            shuttle_times = []
            for name in re.findall('</i>(.+?)</span>', infohtml):
                shuttle_names.append(name)
                start_ind = infohtml.find(name)
                time_string = infohtml[start_ind:start_ind+400]

                print(time_string, '\n')###
                #rgb(255, 234, 63);"> 31-37 min</span>
                #rgb(255, 255, 255);"> no vehicles</span>
                time = re.search('rgb(255, 234, 63);">(.+?)</span>', time_string).group(1)
                print(time)
                #time = '3 min'###

                shuttle_times.append(time)
            print(shuttle_names)###
            print(shuttle_times)###
            shuttle_info = {}
            for i in range(len(shuttle_times)):
                if shuttle_times[i] is not None:
                    shuttle_info[shuttle_names[i]] = shuttle_times[i]
        except AttributeError:
            shuttle_info = None
    except NoSuchElementException:
        print('element not found')
    driver.quit()
    return shuttle_info
    
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
            shut_info = scrapePassio(stop_name)
            response = '\n\nArriving shuttles:\n'
            if shut_info is not None:
                for shuttle in shut_info:
                    response = response + shuttle+' in '+shut_info[shuttle]+'\n'
            else:
                response = 'no shuttles'
            msg = client.messages.create(to=request.values.get("From"), from_=request.values.get("To"),
                                            body=response)
            responded = True
            break

    if not responded:
        msg = client.messages.create(to=request.values.get("From"), from_=request.values.get("To"),
                                         body='Please text me a shuttle stop to get updates!')
    return response

if __name__ == '__main__':
    #app.run()
    scrapePassio('quad') 
    
