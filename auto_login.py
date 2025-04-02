# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0098BF424A739CA09D205BD88D26DDC1264E4BD3423F36583204539A39C4212D03F6B105F356A28A609DA7FBF167B6634FDC002C2359EBA69F1D40F06FFFADA9B0269E69DDE324E751F162779662C88876542ECDEBC3A8EAD5250748EDFECB1569A516115AC1558A262F1806167BEB7659B3D8B4E5CEFB1AF39274498436743E58FF113D98AF88EB4FA6123E6EC91EC81432FEBD942E49D86FD2DC4FDDF6A028BFD30A31FA1EBD84838A41805A27006FDFE484FE18F5171D8059C02325699782C84970D70916B08D425526EFB7AD010171968326E3F374521456DEF06595F20F7C7E009444EDBBD0E83FDB84180CC5C9D87C56F80F55942826858140E0FA0F560AF862A96630B9A31E9EC66930CB872F75D324C31501B63BA7294C1FD273DBE452BF2D27928018D5C6C943777F7B44232A6CA8B51E1BB845DA8E9F88685A997DAD67C4F34028C38192E8F9DCED4E7ABBCE"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
