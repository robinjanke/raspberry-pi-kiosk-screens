from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys


def launch_jira(driver):
    email = open("data/jira_user.txt", "r").read()
    password = open("data/jira_password.txt", "r").read()
    url = open("data/jira_url.txt", "r").read()
    dashboard = open("data/jira_dashboard.txt", "r").read()

    driver.get(url)

    email_input = driver.find_element_by_id("username")
    email_input.send_keys(email)
    email_input.send_keys(Keys.ENTER)
    time.sleep(3)
    password_input = driver.find_element_by_id("password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(10)

    driver.get("{}/plugins/servlet/Wallboard/?dashboardId={}".format(url, dashboard))


def launch_jenkins(driver):
    username = open("data/jenkins_user.txt", "r").read()
    password = open("data/jenkins_password.txt", "r").read()
    url = open("data/jenkins_url.txt", "r").read()
    view = open("data/jenkins_view.txt", "r").read()

    driver.get(url)

    time.sleep(3)
    username_input = driver.find_element_by_name("j_username")
    username_input.send_keys(username)
    time.sleep(3)
    password_input = driver.find_element_by_name("j_password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(10)

    driver.get("{}/view/{}".format(url, view))


if __name__ == "__main__":
    mode = open("data/mode.txt", "r").read()

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
    driver = webdriver.Chrome(options=options)

    if mode == "jira":
        launch_jira(driver)
    elif mode == "jenkins":
        launch_jenkins(driver)
    else:
        raise Exception("Not supported")
