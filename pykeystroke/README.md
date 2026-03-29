# Keystroke Tracker

## Usage
This script is used for windows OS
- Press Ctrl+Shift+Alt+F12 to cancel the script while it's running

## Import the necessary python libraries through pip:
- pynput
- winotify

## Setting up Task Manager
Set up a task to run the script every time you **startup** your computer (**waking up from sleep doesn't count**)
1. Press windows + r to run an application
2. `taskschd.msc`
3. Create Task (Not Create Basic Task)
4. Set up a Trigger
    - Go to the Trigger Menu
    - Create New Trigger
    - Set mode to `At Log On`
    - Optional: Set specific user
5. Set up the action
    - Go to the Actions menu
    - Create New Action
    - Set mode to `Start a Program`
    - Find your pythonw.exe (usually found in C:\Users\darri\AppData\Local\Programs\Python)
    - Set Program/script to the full pythonw.exe path
    - Find the location of the `main.pyw` script in this folder
    - In `Add arguments` paste the entire file path of `main.pyw`
6. Set Conditions
    - Make sure both power and idle options are **OFF**
        - "Start the task only if the computer is idle"
        - "Start the task only if the computer is on AC power"
7. Confirm Settings
    - Go to Settings Menu
    - Disable "Stop the task if it runs longer than 3 days"
    - At the bottom make sure it says: "If the task is already running, **Do not start a new Instance**"
8. Manually Run the Task
    - Right click on the task --> run