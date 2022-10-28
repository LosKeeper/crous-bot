import interactions
from datetime import datetime

# Import all the functions from the other files and variables
from config import TOKEN, CHANNEL
from html_parse import *

# Force tu use english month
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Define the bot
bot = interactions.Client(token=TOKEN,
                          intents=interactions.Intents.ALL)


# Define the command /menu
@bot.command(name='menu', description='Print today\'s menu')
async def _menu(ctx: interactions.CommandContext):
    day = datetime.now().strftime("%d")
    month = datetime.now().strftime("%B")
    month = EN_to_FR(month)
    year = datetime.now().strftime("%Y")
    date = day + " " + month + " " + year

    embed = interactions.Embed(title="Menu RU Illkirch",
                               description="__**"+date+"**__"+"\n```yaml\n"+parse_html(get_html())+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await ctx.send(embeds=embed)


@ bot.event
async def on_start():
    # When bot is ready send menu to the channel
    day = datetime.now().strftime("%d")
    month = datetime.now().strftime("%B")
    month = EN_to_FR(month)
    year = datetime.now().strftime("%Y")
    date = day + " " + month + " " + year
    channel = await bot._http.get_channel(CHANNEL)
    channel = interactions.Channel(**channel, _client=bot._http)
    await channel.purge(amount=10)
    embed = interactions.Embed(title="Menu RU Illkirch",
                               description="__**"+date+"**__"+"\n```yaml\n"+parse_html(get_html())+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await channel.send(embeds=embed)


bot.start()
