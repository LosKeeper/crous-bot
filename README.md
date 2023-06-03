# <img src="assets/icon.svg" alt="icon" width="4%"/> Discord Calendar Bot
[![Github Version](https://img.shields.io/github/v/release/loskeeper/discord-menu-bot)](https://github.com/LosKeeper/discord-menu-bot)
[![Github License](https://img.shields.io/github/license/loskeeper/discord-menu-bot)](https://github.com/LosKeeper/discord-menu-bot/blob/main/LICENSE)
[![Github Last Commit](https://img.shields.io/github/last-commit/loskeeper/discord-menu-bot)](https://github.com/LosKeeper/discord-menu-bot/commits)
[![Github Issues](https://img.shields.io/github/issues/loskeeper/discord-menu-bot)](https://github.com/LosKeeper/discord-menu-bot/issues)

[![Python Version](https://img.shields.io/pypi/pyversions/discord-py-interactions)](https://www.python.org/downloads/)
[![Interactions.py Version](https://img.shields.io/badge/interactions.py-v5-green)](https://github.com/interactions-py/interactions.py)

[![Author](https://img.shields.io/badge/author-@LosKeeper-blue)](https://github.com/LosKeeper)
> This bot is used to display the menu of the Crous in a discord channel and to send the menu at a specific time of the day.

## 🧾 Table of Contents
1. [🔧 Setup](#-setup)
2. [🚀 Launch](#-launch)
3. [📝 Commands](#-commands)
4. [🐞 Bugs and TODO](#-bugs-and-todo)


## 🔧 Setup
> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/warning.svg">
>   <img alt="Warning" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/warning.svg">
> </picture><br>
>
> You need to have installed en_US locale on your system to make the bot work.
> If you don't have it, you can install it with the following command :
> ```bash
> sudo locale-gen en_US.UTF-8
> ```

Many libraries are needed to make this bot work :
```bash
pip install -r requirements.txt
```
> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/info.svg">
>   <img alt="Info" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/info.svg">
> </picture><br>
>
> If you have some troubles with the installation of the `pycurl` library, make sure to have installed the `libcurl4-openssl-dev` and the `libssl-dev` packages :
> ```bash
> sudo apt install libcurl4-openssl-dev libssl-dev
> ```

To configure the bot, you need to create configuration file name `.env` (you can use the `.env.example` file as a template) :
```ini
# URL of the menu of the restaurants
URL_ILLKIRCH=""
URL_CRONENBOURG=""
URL_PAUL_APPELL=""

# Token of the bot
TOKEN=""

# ID of the channel where the bot will send the menu and ID of the owner of the bot to use /echo
CHANNEL_ID=""
OWNER_ID=""

# Hour of the day when the bot will send the daily message (24h format):
HOUR=
MINUTE=
```


## 🚀 Launch
To launch the bot, you need to run the `main.py` file :
```bash
python3 main.py
```

## 📝 Commands
The bot use the slash commands to interact with the user.
| Command             | Description                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------- |
| `/menu`             | Get the list of all the available menus for the day and the menus for tomorrow passed 14:00.            |
| `/menu illkirch`    | Get the menu of the Illkirch restaurant.                                                                |
| `/menu cronenbourg` | Get the menu of the Cronenbourg restaurant.                                                             |
| `/menu paul appell` | Get the menu of the Paul Appell restaurant.                                                             |
| `/echo <message>`   | Send a message in the channel choosed by CHANNEL_ID (only for the owner of the bot using the OWNER_ID). |

In adition, the bot send a message at a specific time mentioned in the `.env` file with the menu of the day and the menu of tomorrow passed 14:00.

## 🐞 Bugs and TODO
- [ ] Add test for the bot
- [ ] Make code cleaner and more compact
- [ ] Add logs
