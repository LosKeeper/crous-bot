import interactions
from datetime import datetime

# Import all the functions from the other files and variables
from config import TOKEN, CHANNEL, URL_CRONENBOURG, URL_ILLKIRCH
from html_parse import *

# Force tu use english month
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Define the bot
bot = interactions.Client(token=TOKEN,
                          intents=interactions.Intents.ALL)


# Define the command /menu
@bot.command(name='menu', description='Print today\'s menu',
             options=[interactions.Option(
                 name='name',
                 description='Name of the RU (Cronenbourg or Illkirch)',
                 type=interactions.OptionType.STRING,
                 required=False)])
async def _menu(ctx: interactions.CommandContext, name: str = None):

    # If the user didn't specify the name of the RU
    if name is None:
        name = "Illkirch"
        url = URL_ILLKIRCH
    elif name.lower() == "illkirch":
        name = "Illkirch"
        url = URL_ILLKIRCH
    elif name.lower() == "cronenbourg":
        name = "Cronenbourg"
        url = URL_CRONENBOURG
    else:
        await ctx.send("This RU doesn't exist or is not supported yet !")
        return

   # Get the date
    day = datetime.now().strftime("%d")

    if day[0] == "0":
        day = day[1]

    month = datetime.now().strftime("%B")
    month = EN_to_FR(month)

    # If the time is after 14h, the menu is for the next day
    hour = datetime.now().strftime("%H")
    if int(hour)+delta_time >= 14:
        day_int = int(day)+1
    else:
        day_int = int(day)

    date = "%s" % day_int + " "+month

    embed = interactions.Embed(title="Menu RU "+name,
                               description="__**"+date+"**__"+"\n```yaml\n"+parse_html(get_html(url))+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await ctx.send(embeds=embed)


# Print menu at startup
@bot.event
async def on_start():
    # When bot is ready send menu to the channel
    # Get the date
    day = datetime.now().strftime("%d")

    if day[0] == "0":
        day = day[1]

    month = datetime.now().strftime("%B")
    month = EN_to_FR(month)

    # If the time is after 14h, the menu is for the next day
    hour = datetime.now().strftime("%H")
    if int(hour)+delta_time >= 14:
        day_int = int(day)+1
    else:
        day_int = int(day)

    date = "%s" % day_int + " "+month
    channel = await bot._http.get_channel(CHANNEL)
    channel = interactions.Channel(**channel, _client=bot._http)
    await channel.purge(amount=10)
    embed = interactions.Embed(title="Menu RU Illkirch",
                               description="__**"+date+"**__"+"\n```yaml\n"+parse_html(get_html(URL_ILLKIRCH))+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await channel.send(embeds=embed)


bot.start()
