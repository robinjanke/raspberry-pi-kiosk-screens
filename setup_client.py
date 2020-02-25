import subprocess
import os
import time

jira_username_filename = "data/jira_user.txt"
jira_password_filename = "data/jira_password.txt"
jira_url_filename = "data/jira_url.txt"
jira_dashboard_filename = "data/jira_dashboard.txt"

jenkins_url_filename = "data/jenkins_url.txt"
jenkins_password_filename = "data/jenkins_password.txt"
jenkins_username_filename = "data/jenkins_user.txt"
jenkins_view_filename = "data/jenkins_view.txt"

webdriver_path = ""
script_filename = "launch_dashboard.py"
launch_dashboard_filename = "launch_dashboard.desktop"
launch_dashboard_filename_etc = "/etc/xdg/autostart/launch_dashboard.desktop"
mode_filename = "data/mode.txt"


def ask_and_write_to_file(text, filename):
    print("Please enter: {}".format(text))
    content = input()
    file = open(filename, "w+")
    file.write(content)


def ask_for_mode():
    print("Please enter your mode: jenkins or jira")
    mode = input()
    if mode == "jenkins":
        print("Using mode jenkins")
    elif mode == "jira":
        print("Using mode jira")
    else:
        ask_for_mode()
    file = open(mode_filename, "w+")
    file.write(mode)
    return mode


def setup_jira():
    ask_and_write_to_file("Jira username", jira_username_filename)
    ask_and_write_to_file("Jira password", jira_password_filename)
    ask_and_write_to_file("Jira url (https://xxx.atlassian.net)", jira_url_filename)
    ask_and_write_to_file("Jira dashboard ID", jira_dashboard_filename)


def setup_jenkins():
    ask_and_write_to_file("Jenkins username", jenkins_username_filename)
    ask_and_write_to_file("Jenkins password", jenkins_password_filename)
    ask_and_write_to_file("Jenkins url (https://jenkins.example.com)", jenkins_url_filename)
    ask_and_write_to_file("Jenkins view name (can be found in the url)", jenkins_view_filename)


def setup():
    print("Installing pip packages start")
    subprocess.check_output(["/bin/bash", "-c", "pip3", "install" "-r", "requirements.txt"])

    print("Running apt-get update")
    subprocess.check_output(["sudo", "apt-get", "update", "-y"])

    print("Installing packages with apt-get")
    for package in ["chromium-driver", "ufw", "vim", "unclutter"]:
        subprocess.check_output(["sudo", "apt-get", "install", "-y", package])

    mode = ask_for_mode()

    if mode == "jira":
        setup_jira()
    elif mode == "jenkins":
        setup_jenkins()

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


if __name__ == "__main__":
    setup()
