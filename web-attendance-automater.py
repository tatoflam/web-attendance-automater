import argparse
import platform
import time
import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from const import URL, COMPANY_ID, ID, PASSWORD, COMPANY_ID_XPATH, \
    ID_XPATH, PASSWORD_XPATH, LOGIN_XPATH, ATTENDANCE_TABLE, LOGOFF_XPATH, \
    ARG_COME, ARG_LEAVE, COME, LEAVE, PUNCH, PATH_CHROMEDRIVER
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

def main():
    # Parse parameter
    parser = argparse.ArgumentParser()
    parser.add_argument('--parameter', type=str, 
                        help='specify "come" or "leave"')
    args = parser.parse_args()
    status = args.parameter
    
    if not status in [ARG_COME,ARG_LEAVE]:
        print('please set argument as "come" or "leave"')
    else: 
        dt_now = datetime.datetime.now()
        print('%s : Web attendance automater start' % dt_now)

        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless") # if you want it headless	
        
        if platform.system() == "Linux" and (platform.machine() == "armv6l" or platform.machine() == "armv7l"):  
            # if raspi 32 bit
            options.BinaryLocation = ("/usr/bin/chromium-browser")
            service = Service("/usr/bin/chromedriver") 
        else:
            # if not raspi, using Chrome
            service = Service(ChromeDriverManager().install()) 

        # web driver manager for Chromium only supports linux 64 bit version
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
        
        driver = webdriver.Chrome(service=service, options=options)

        # Login
        driver.get(URL)
        driver.find_element(By.XPATH, COMPANY_ID_XPATH).send_keys(COMPANY_ID)
        driver.find_element(By.XPATH, ID_XPATH).send_keys(ID)
        driver.find_element(By.XPATH, PASSWORD_XPATH).send_keys(PASSWORD)
        
        wait = WebDriverWait(driver, 5)
        
        if EC.element_to_be_clickable((By.XPATH, LOGIN_XPATH)):
            print('Login is clickable')
        
        driver.find_element(By.XPATH, LOGIN_XPATH).click()
        print('Login completed')

        # Punch
        wait.until(EC.presence_of_element_located((By.XPATH, ATTENDANCE_TABLE)))

        if status == ARG_COME:
            driver.find_element(By.XPATH, COME).click()            
            print('Come is clicked')
        elif status == ARG_LEAVE:
            driver.find_element(By.XPATH, LEAVE).click()
            print('Leave is clicked')
        time.sleep(3)

        if EC.element_to_be_clickable((By.XPATH, PUNCH)):
            print('Punch is clickable')
            driver.find_element(By.XPATH, PUNCH).click()
            print('Punch completed')
        time.sleep(5)

        # Logoff        
        if EC.element_to_be_clickable((By.XPATH, LOGOFF_XPATH)):
            print('Logoff is clickable')

        driver.find_element(By.XPATH, LOGOFF_XPATH).click()
        print('Logoff completed')
        driver.close()
        
        dt_end = datetime.datetime.now()
        print('%s : Web attendance automater end' % dt_end)
    
if __name__ == "__main__":
    main()
