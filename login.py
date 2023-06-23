from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
from os import environ as os_environ


def login():
    chrome_options = ChromeOptions()
    chrome_options.binary_location = os_environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = Chrome(executable_path=os_environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    # driver=Chrome(executable_path='C:\Python\chromedriver.exe')
    driver.get('https://www.cybercoders.com/')  # navigating to the homepage
    sleep(3)
    driver.find_element(by=By.XPATH,
                        value='//button[@id="onetrust-accept-btn-handler"]').click()  # accepting all cookies
    driver.find_element(by=By.XPATH, value='//span[@data-type="login"]').click()  # navigating to the login page
    sleep(3)

    # locating the email and password text fields
    email = driver.find_element(by=By.XPATH, value='//input[@class="global-email-icon email-input"]')
    password = driver.find_element(by=By.XPATH, value='//input[@class="global-password-icon"]')

    email.send_keys("ENTER USERNAMe")  # type your own username here
    password.send_keys("ENTER PASSWORD")  # type your own password here

    # submitting the login credentials
    driver.find_element(by=By.XPATH, value='//input[@id="login-signup-submit"]').click()
    sleep(5)
    print('LOGIN DONE')
    driver.get('https://www.cybercoders.com/search/')
    return driver
