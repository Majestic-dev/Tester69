# Tester69

[![](https://discord.com/api/guilds/733219077744754750/embed.png)](https://discord.gg/VsDDf8YKBV)

A general-use discord bot coded in discord.py

# Big shoutout to [kaJob-dev](https://github.com/kaJob-dev) (kajob. on discord) for guiding me on this project!

# Installation

## Clone the [repository](https://github.com/Majestic-dev/Tester69/)
```bash
git clone https://github.com/Majestic-dev/Tester69.git
```

## Install [requirements.txt](requirements.txt)
```bash
pip install -r requirements.txt
```
or
```bash
python -m pip install -r requirements.txt
```

## Running the bot

### change your current directory to the cloned repository
```bash
cd Tester69
```

v1.2
### run the file
```bash
python main.py
```

# Contributing 
All contributions are welcome! If you'd like to contribute, please make a pull request.

Please make sure that your code is formatted correctly before making a new pull request. This project is formatted using [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) to sort imports. Read through open and closed pull requests and ensure that no one else has already made a similar pull request. 

# License 
This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details

v1.2
# Version Changelogs

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
        * Use the dispatch event for certain actions

    - Miscellaneous
        * Many miscellaneous commands to search random stuff, get random images, gifs, etc.

    - Commands
        * Cooldowns for most commands using discord's built in cooldown system
        * Cooldowns using the new cooldown handler for longer duration commands (hourly, daily, weekly, monthly)

    - Economy
        * Updated all the economy items and a command to view the descriptions of items
        * Banking system and a global leaderboard
        * Archived all gambling commands to ensure a safe future for Tester69 on discord, and blackjack being broken anyways
    
    - Database
        * Migrated from a JSON database (if you call it a one) to PostgreSQL (asyncpg)

# TODO

## V1.3 Focused On Reworking Some Systems

- [ ] Rework the Economy system to be more fun and interactive