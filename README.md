# Tester69

[![](https://discord.com/api/guilds/733219077744754750/embed.png)](https://discord.gg/VsDDf8YKBV)

A general-use discord bot coded in discord.py

# Big shoutout to kaJob-dev on github (Jakob#2222 on discord) for guiding me on this project!

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

### Guide
1. Clone the repository
2. Run the main.py file

    Running the main.py file for the first time will create a new directory named "data" and 3 new files in it. It should then ask you to enter your bot token. You can see how to get a bot token [here](https://www.youtube.com/watch?v=aI4OmIbkJH8). There will also be a new directory named "fonts", there you can place any fonts you'd like that have the .ttf extension. This will be used for [Pillow](https://pillow.readthedocs.io/en/stable/index.html#) image generation for the verification system. Enter your bot token in the data/config.json file and save the file. Then run the main.py file again. It should now work. If you don't want to run the main file in a code editor you can run it using the [start.bat](start.bat) file.

# Contributing 
All contributions are welcome! If you'd like to contribute, please make a pull request.

Please make sure that your code is formatted correctly before making a new pull request. This project is formatted using [black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) to sort imports. Read through open and closed pull requests and ensure that no one else has already made a similar pull request. 

# License 
This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details

# Version Changelogs

## v1.1

    - Verification System
        * Optimised verification system setup (now only requires 1 command)
        * Made the verification system more secure (code will be on images that are noisy and blurred)
        * After the first startup you can add more fonts to the fonts folder (has to be a .ttf file)
        * You can now disable verification if you wish to
    
    - Warning System
        * Warnings are now per server, not global
    
    - Server Management
        * Added a word blacklist (blacklist the words you don't want being sent)
        * Added a user/role whitelist (whitelist the users/roles you want to be able to bypass the word blacklist)
        * Added a welcome message that will be sent to users when they join the server (if a server has enabled verification, it will be sent after they verify)
    
    - Main Commands
        * Updated the help command to list all the commands

    - Economy
        * Changed the add and subtract commands to text commands, because a way to abuse it was found (change the guild permissions of that command)
    
    - Logging System
        * More things are now logged (message deletion, message editing). This will be improved and updated

    - Main
        * On first startup, a new folder (fonts) will be created

    - Listeners
        * Moved some listeners to another file to make other files smaller in size

## v1.2

    - Moderation System
        * Made muting and unmuting more efficient
            * Muted role will be set using a command (/set_muted_role)
            * Before a member gets muted, their roles get saved, when muted their roles will be replaced with the set muted role
            * When unmuted, their roles will be replaced with the roles they had before they got muted
    

# TODO

## v1.2 Focused On Economy And Some Fixes/Reworking To Moderation

- [x] Add some customization to the moderation system (for example setting the muted role).
- [ ] Migrate from json to a binary database.
- [ ] Add a shop for economy.
- [ ] Redo fishing and hunting.
- [ ] Add a way to auction things (basically like Dank Memer).
- [ ] More gambling games.

## V1.3 Focused On Miscellaneous/Fun

- [ ] Think of the update notes for this version.