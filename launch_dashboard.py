from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys

email = open("data/jira_user.txt", "w+").read()
password = open("data/jira_password.txt", "w+").read()
url = open("data/jira_url.txt", "w+").read()
dashboard = open("data/jira_dashboard.txt", "w+").read()

options = webdriver.ChromeOptions()
options.add_argument(argument="-kiosk")
options.add_argument(argument="--no-sandbox")
options.add_argument(argument="--disable-dev-shm-usage")
options.add_argument(argument="--disable-gpu")
options.add_argument(argument="--window-size=1920,1080")
options.add_argument(argument="disable-infobars")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
})

chromedriver = webdriver.Chrome(options=options)
chromedriver.get(url)

email_input = chromedriver.find_element_by_id("username")
email_input.send_keys(email)
email_input.send_keys(Keys.ENTER)
time.sleep(3)
password_input = chromedriver.find_element_by_id("password")
password_input.send_keys(password)
password_input.send_keys(Keys.ENTER)
time.sleep(10)

chromedriver.get("{}/plugins/servlet/Wallboard/?dashboardId={}".format(url, dashboard))