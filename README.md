# Tester69

[![](https://discord.com/api/guilds/733219077744754750/embed.png)](https://discord.gg/VsDDf8YKBV)

A general-use discord bot coded in discord.py

# Big shoutout to [kaJob-dev](https://github.com/kaJob-dev) (kajob. on discord) for guiding me on this project!

# Installation

```bash
# Clone the repository
git clone https://github.com/Majestic-dev/Tester69.git

# Install the requirements
pip install -r requirements.txt

# Change the directory
cd Tester69

# Run the bot
python main.py
```

# Community Standards

[Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)

[Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)

[Code Of Conduct](.github/CODE_OF_CONDUCT.md)

[Contributing Guidelines](.github/CONTRIBUTING.md)

[License](LICENSE)

[Code Security](.github/SECURITY.md)

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

## v1.3

    - Miscallaneous
        * Added a giveaway system (including ending the giveaway immediately, rerolling the giveaway, etc.)
        * Added discord's logging, everything will be logged in the specified file

    - Server(management)
        * Added a ticket system with a panel that guides you through the setup

    - Database
        * Added a separate database for the giveaways
        * Added a function to create a database backup

# TODO

## V1.3 Focused On Reworking Some Systems

- [x] Add a Giveaway system
- [x] Add a ticket system
- [ ] Create my own paginator
- [ ] Rework the Economy system to be more fun and interactive