import argparse
import platform
import time
import datetime
import json
import random
from logging import config, getLogger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from const import URL, COMPANY_ID, ID, PASSWORD, COMPANY_ID_XPATH, \
    ID_XPATH, PASSWORD_XPATH, LOGIN_XPATH, ATTENDANCE_TABLE, LOGOFF_XPATH, \
    ARG_COME, ARG_LEAVE, ARG_BREAK_START, ARG_BREAK_END, \
    COME, LEAVE, BREAK_START, BREAK_END, PUNCH, PATH_CHROMEDRIVER
from util import LOGGING_CONF, isBusinessDay, isVacation
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

config_dict = None
with open(LOGGING_CONF, 'r', encoding='utf-8') as f:
    config_dict = json.load(f)

config.dictConfig(config_dict)
logger = getLogger(__name__)

def login(driver):
    driver.get(URL)
    driver.find_element(By.XPATH, COMPANY_ID_XPATH).send_keys(COMPANY_ID)
    driver.find_element(By.XPATH, ID_XPATH).send_keys(ID)
    driver.find_element(By.XPATH, PASSWORD_XPATH).send_keys(PASSWORD)
    
    if EC.element_to_be_clickable((By.XPATH, LOGIN_XPATH)):
        logger.info('Login is clickable')
    
    driver.find_element(By.XPATH, LOGIN_XPATH).click()
    logger.info('Login completed')
    
def punch(driver, status):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, ATTENDANCE_TABLE)))

    if status == ARG_COME:
        driver.find_element(By.XPATH, COME).click()            
        logger.info('Come is clicked')
    elif status == ARG_LEAVE:
        driver.find_element(By.XPATH, LEAVE).click()
        logger.info('Leave is clicked')
    elif status == ARG_BREAK_START:
        driver.find_element(By.XPATH, BREAK_START).click()
        logger.info('Break Start is clicked')
    elif status == ARG_BREAK_END:
        driver.find_element(By.XPATH, BREAK_END).click()
        logger.info('Break End is clicked')
    
    waitsec = random.randint(0,600)
    logger.info('Wait : %d sec' % waitsec)

    time.sleep(waitsec)

    if EC.element_to_be_clickable((By.XPATH, PUNCH)):
        logger.info('Punch is clickable')
        driver.find_element(By.XPATH, PUNCH).click()
        logger.info('Punch completed')

def logoff(driver):
    if EC.element_to_be_clickable((By.XPATH, LOGOFF_XPATH)):
        logger.info('Logoff is clickable')

    driver.find_element(By.XPATH, LOGOFF_XPATH).click()
    logger.info('Logoff completed')
    driver.close()
    
def main():
    # Parse parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('--parameter', type=str, 
                        help='specify "come", "leave", "break_start", or "break_end"')
    args = parser.parse_args()
    status = args.parameter

    dt_today = datetime.date.today()    
    if not status in [ARG_COME,ARG_LEAVE,ARG_BREAK_START,ARG_BREAK_END]:
        logger.info('please set an argument as "come", "leave", "break_start", or "break_end"')
    elif not isBusinessDay(dt_today):
        logger.info('Pass attendance as %s is not a business day' % dt_today)
    elif isVacation(dt_today):
        logger.info('Pass attendance as %s is vacation' % dt_today)
    else: 
        logger.info('Web attendance automater start')

        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless") # if you want it headless	
        
        if platform.system() == "Linux" and \
          (platform.machine() == "armv6l" or \
           platform.machine() == "armv7l"):  
            # if raspi 32 bit
            options.BinaryLocation = ("/usr/bin/chromium-browser")
            service = Service("/usr/bin/chromedriver")
            logger.info('Using local chromedriver') 
        else:
            # if not raspi, using Chrome
            service = Service(ChromeDriverManager().install()) 
            logger.info('Using chromedriver installed by ChromeDriverManager')

        # web driver manager for Chromium only supports linux 64 bit version
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        
        driver = webdriver.Chrome(service=service, options=options)

        # Login
        login(driver)

        # Punch
        punch(driver, status)

        # Logoff 
        logoff(driver)
        
        logger.info('Web attendance automater end')

if __name__ == "__main__":
    main()
