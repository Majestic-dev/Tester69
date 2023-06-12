# Tester69

[![](https://discord.com/api/guilds/733219077744754750/embed.png)](https://discord.gg/VsDDf8YKBV)

A general-use discord bot coded in discord.py

# Big shoutout to kaJob-dev on github (Jakob#2222 on discord) for guiding me on this project!

# ENJOY YOUR SUMMER ❤️, THIS HAS BEEN THE BEST 5 MONTHS OF MY CODING JOURNEY! SEE YOU IN SEPTEMBER!


## Project on hold until September ❤️, see you soon!

# Installation
### Requirements
- [Python 3.8 or higher](https://www.python.org/downloads/)
- discord.py, version 2.1.0 or higher 
    ```bash
    # WINDOWS 
    python -m pip install -U discord.py

    # LINUX
    python3 -m pip install -U discord.py

    # MACOS
    python3 -m pip install -U discord.py
    ```
- Python Pillow (Install with pip)
    ```bash
    # WINDOWS 
    pip install pillow

    # LINUX
    pip3 install pillow

    # MACOS
    pip3 install pillow
    ```

## Guide

### Clone the repository
```bash
git clone https://github.com/Majestic-dev/Tester69.git
```

### Install requirements.txt
``bash
pip install -r requirements.txt
```
or
```bash
python -m pip install -r requirements.txt
```

### Running the bot through VSCode

Install Pylance and Python extensions on github, after you've done that you should be able to run the main.py file by clicking the "Run Python File" button in the top right corner of the screen

### Running the bot through terminal

change your current directory to the cloned repository
```bash
cd Tester69
```

run the file
```bash
python main.py
```

# Contributing 
All contributions are welcome! If you'd like to contribute, please make a pull request.

Please make sure that your code is formatted correctly before making a new pull request. This project is formatted using [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) to sort imports. Read through open and closed pull requests and ensure that no one else has already made a similar pull request. 

# License 
This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details

# Version Changelogs

## v1.1

    - Verification System
        * Optimized and improved the verification system
    
    - Warning System
        * Warnings are now per server, not global
    
    - Server Management
        * Improved the server management system (adding/removing blacklisted words and whitelisted users/roles)
    
    - Main Commands
        * Updated the help command to list all the commands

    - Economy
        * Improve the security of some commands
    
    - Logging System
        * A logging system to log server actions

## v1.2

    - Moderation System
        * Improved muting and unmuting

    - Logging System
        * Log deletion protection

    - Miscellaneous
        * Many miscellaneous commands to search random stuff, get random images, gifs, etc.

    - Commands
        * Cooldowns for most commands using discord's built in cooldown system

    - Economy
        * Updated all the economy items and a command to view the descriptions of items
        * Banking system and a global leaderboard

# TODO

## v1.2 Focused On Economy And Miscallaneous Systems

- [x] Add some customization to the moderation system (for example setting the muted role).
- [x] Add a way to deposit/withdraw money into the bank.
- [ ] Migrate from json to a more reliable database.
- [ ] Make a custom cooldown handler for a few commands (hourly, daily, weekly and monthly).

## V1.3 Focused On Miscellaneous/Fun

- [ ] Think of the update notes for this version.