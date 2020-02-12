import subprocess
import os
import time


def ask_and_write_to_file(text, filename):
    print("Please enter: {}".format(text))
    content = input()
    file = open(filename, "w+")
    file.write(content)


jira_username_filename = "data/jira_user.txt"
jira_password_filename = "data/jira_password.txt"
jira_url_filename = "data/jira_url.txt"
jira_dashboard_filename = "data/jira_dashboard.txt"

webdriver_path = ""
script_filename = "launch_dashboard.py"
launch_dashboard_filename = "launch_dashboard.desktop"
launch_dashboard_filename_etc = "/etc/xdg/autostart/launch_dashboard.desktop"

print("Installing pip packages start")
subprocess.check_output(["/bin/bash", "-c", "pip3", "install" "-r", "requirements.txt"])

print("Running apt-get update")
subprocess.check_output(["sudo", "apt-get", "update", "-y"])

print("Installing packages with apt-get")
for package in ["chromium-driver", "ufw", "vim"]:
    subprocess.check_output(["sudo", "apt-get", "install", "-y", package])

ask_and_write_to_file("Jira username", jira_username_filename)
ask_and_write_to_file("Jira password", jira_password_filename)
ask_and_write_to_file("Jira url (https://xxx.atlassian.net)", jira_url_filename)
ask_and_write_to_file("Jira dashboard ID", jira_dashboard_filename)

print("Setup autostart to launch {} file".format(script_filename))
dashboard_file = open(launch_dashboard_filename, "r")
current_dir = os.path.dirname(os.path.realpath(__file__))
dashboard_file_content = dashboard_file.read()
dashboard_file_content = dashboard_file_content.format(CURRENT_DIR=current_dir, FILENAME=script_filename)
subprocess.check_output(["sudo", "touch", launch_dashboard_filename_etc])
subprocess.check_output(["sudo", "chmod", "0777", launch_dashboard_filename_etc])
subprocess.check_output(["sudo", "chown", "root:root", launch_dashboard_filename_etc])
open(launch_dashboard_filename_etc, "w+").write(dashboard_file_content)
subprocess.check_output(["sudo", "chmod", "0755", launch_dashboard_filename_etc])

for second in range(10, 0):
    print("Rebooting in {} seconds".format(second))
    time.sleep(1)

print("Rebooting now")
subprocess.check_output(["sudo", "reboot"])
