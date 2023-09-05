import interactions

from datetime import datetime

from dotenv import load_dotenv
from os import environ as env

from api_parse import *

# Force to use english month
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Load the .env file
load_dotenv()

# Define the bot
bot = interactions.Client(token=env["TOKEN"],
                          intents=interactions.Intents.ALL)

# Define and get the json var
illkirch = json_to_dict(get_html(env["URL_API"]+"/illkirch"))
cronenbourg = json_to_dict(get_html(env["URL_API"]+"/cronenbourg"))
paul_appell = json_to_dict(get_html(env["URL_API"]+"/paul-appell"))


# Define the command /echo
@interactions.slash_command(name="echo", description="Echo a message")
@interactions.slash_option(name="message", description="The message to echo",
                           required=True, opt_type=interactions.OptionType.STRING)
async def _echo(ctx: interactions.SlashContext, message: str):
    # Check for the owner
    if int(ctx.author.id) != int(env["OWNER_ID"]):
        print(ctx.author.id)
        print(env["OWNER_ID"])
        return await ctx.send("You cannot do this, only the owner can !")
    channel = await bot.fetch_channel(env["CHANNEL_ID"])
    await ctx.respond("Message sent in the channel #"+channel.name+" on the server "+channel.guild.name+" ! ")
    await channel.send(message)


# Define the command /menu
@interactions.slash_command(name='menu', description='Print today\'s menu')
@interactions.slash_option(name='name',
                           description='Name of the RU (Cronenbourg or Illkirch or Paul-Appell)',
                           opt_type=interactions.OptionType.STRING,
                           choices=[
                                interactions.SlashCommandChoice(
                                    name="Illkirch", value="Illkirch"),
                                interactions.SlashCommandChoice(
                                    name="Cronenbourg", value="Cronenbourg"),
                                interactions.SlashCommandChoice(
                                    name="Paul-Appell", value="Paul-Appell")
                           ],
                           required=True)
async def _menu(ctx: interactions.SlashContext, name: str = None):

    # If the user didn't specify the name of the RU
    if name is None:
        name = "Illkirch"
        print_ru = print_illkirch
        ru = illkirch
    elif name.lower() == "illkirch":
        name = "Illkirch"
        print_ru = print_illkirch
        ru = illkirch
    elif name.lower() == "cronenbourg":
        name = "Cronenbourg"
        print_ru = print_cronenbourg
        ru = cronenbourg
    elif name.lower() == "paul-appell" or name.lower() == "paul appell" or name.lower() == "paul":
        name = "Paul-Appell"
        print_ru = print_paul_appell
        ru = paul_appell
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
    if int(hour) >= 14 and name != "Paul-Appell":
        day_int = int(day)+1
    else:
        day_int = int(day)

    date = "%s" % day_int + " "+month

    embed = interactions.Embed(title="Menu RU "+name,
                               description="__**"+date+"**__"+"\n```yaml\n"+print_ru(date, ru)+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await ctx.send(embeds=embed)


@interactions.Task.create(interactions.TimeTrigger(hour=int(env["HOUR"]), minute=int(env["MINUTE"]), utc=False))
async def _daily_menu():

    # Don't print the menu on week-end
    if datetime.now().weekday() in [5, 6]:
        return

    # Get the date
    day = datetime.now().strftime("%d")

    if day[0] == "0":
        day = day[1]

    month = datetime.now().strftime("%B")
    month = EN_to_FR(month)

    # If the time is after 14h, the menu is for the next day
    hour = datetime.now().strftime("%H")
    if int(hour) >= 14:
        day_int = int(day)+1
    else:
        day_int = int(day)

    date = "%s" % day_int + " "+month
    channel = await bot.fetch_channel(env["CHANNEL_ID"])
    await channel.purge(deletion_limit=10)
    embed = interactions.Embed(title="Menu RU Illkirch",
                               description="__**"+date+"**__"+"\n```yaml\n"+print_illkirch(date, illkirch)+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await channel.send(embeds=embed)


@interactions.listen()
async def on_start(event: interactions.api.events.Startup):
    # Change presence
    await bot.change_presence(
        activity=interactions.Activity(
            name="/menu", type=interactions.ActivityType.PLAYING)
    )

    # Start the daily menu
    _daily_menu.start()


# Start the bot
bot.start()
