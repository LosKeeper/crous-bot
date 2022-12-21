# Discord Menu Bot Crous
A simple bot that allows you to create menus in discord.
> This bot uses Paris timezone.

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [List of commands](#list-of-commands)
5. [Contributing](#contributing)
6. [TODO](#todo)

## Installation
You first need to install all the required packages. You can do this by running the following command :
```bash
pip install -r requirements.txt
```
## Configuration
You need to create a file named `config.py` in the root directory of the project. This file will contain all the configuration of the bot. Here is an example of a configuration file :
```py
URL_ILLKIRCH    = "<The URL of the menu of the Illkirch restaurant>"
URL_CRONENBOURG = "<The URL of the menu of the Cronenbourg restaurant>"
URL_PAUL_APPELL = "<The URL of the menu of the Paul Appell restaurant>"
TOKEN           = "<The token of the bot>"
CHANNEL         = "<The channel where the bot will send the menu>"
OWNER_ID        = "<The ID of the owner of the bot>"
```

> **Note:** The URL must be an URL of a Crous website. If you want to use another website, you will need to modify the code. 

## Usage
You can run the bot by running the following command :
```bash
python main.py
```
The bot will then start, send the today's menu in the channel choosed and you can use it by typing `/menu` in a discord channel to get the list of all the available menus for the day.

## List of commands
| Command             | Description                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------- |
| `/menu`             | Get the list of all the available menus for the day and the menus for tomorrow passed 14:00. |
| `/menu illkirch`    | Get the menu of the Illkirch restaurant.                                                     |
| `/menu cronenbourg` | Get the menu of the Cronenbourg restaurant.                                                  |
| `/menu paul appell` | Get the menu of the Paul Appell restaurant.                                                  |
| `/echo <message>`   | Send a message in the channel choosed by CHANNEL_ID (only for the owner of the bot).         |

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## TODO
- [ ] Add a command to get the menu of a specific day.
- [ ] Add dictionary to simplify the commands of the bot.
