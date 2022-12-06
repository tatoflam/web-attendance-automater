from selenium import webdriver
from selenium.webdriver.chrome import service as cs
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from const import URL, COMPANY_ID, ID, PASSWORD, COMPANY_ID_XPATH, \
    ID_XPATH, PASSWORD_XPATH, LOGIN_XPATH, TIME_TABLE, LOGOFF_XPATH, \
    row_str, start_row, date_str, end_time_str, submit_str, end_hour, \
    PATH_CHROMEDRIVER
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import re

def main():
    dt_now = datetime.datetime.now()
    print('%s : Web attendance automater start' % dt_now)
    
    # chrome_service = cs.Service(executable_path=PATH_CHROMEDRIVER)
    # driver = webdriver.Chrome(service=chrome_service)
    driver = webdriver.Chrome(service=cs.Service(ChromeDriverManager().install()))
    driver.get(URL)
    driver.find_element(By.XPATH, COMPANY_ID_XPATH).send_keys(COMPANY_ID)
    driver.find_element(By.XPATH, ID_XPATH).send_keys(ID)
    driver.find_element(By.XPATH, PASSWORD_XPATH).send_keys(PASSWORD)
    
    wait = WebDriverWait(driver, 10)
    
    if EC.element_to_be_clickable((By.XPATH, LOGIN_XPATH)):
        print('clickable')
    
    driver.find_element(By.XPATH, LOGIN_XPATH).click()

    wait.until(EC.presence_of_element_located((By.XPATH, TIME_TABLE)))
    
    pattern = re.compile(r'月|火|水|木|金')
    row = start_row
    
    while True:
        try:
            driver.find_element(By.XPATH, row_str % row)
        except NoSuchElementException:
            print("No more row. The timecard should be up-to-date. ")
            break
        except Exception as e:
            print(e)
                        
        if EC.element_to_be_clickable((By.XPATH, submit_str % row)):
            element = driver.find_element(By.XPATH, date_str % row )
            date = element.text
            if bool(pattern.search(date)):
                print('%s is clickable' % date)
                driver.find_element(By.XPATH, end_time_str % row ).send_keys(end_hour)
                driver.find_element(By.XPATH, submit_str % row).click()
        
        time.sleep(1)
        row +=1

    time.sleep(10)
    
    if EC.element_to_be_clickable((By.XPATH, LOGOFF_XPATH)):
        print('logoff is clickable')

    driver.find_element(By.XPATH, LOGOFF_XPATH).click()   
    driver.close()
    
    dt_end = datetime.datetime.now()
    print('%s : Web attendance automater end' % dt_end)

    
if __name__ == "__main__":
    main()
