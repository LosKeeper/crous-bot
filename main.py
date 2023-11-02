import interactions

from datetime import datetime

from dotenv import load_dotenv
from os import environ as env

from api_parse import *

# Load the .env file
load_dotenv()

# Define the bot
bot = interactions.Client(token=env["TOKEN"],
                          intents=interactions.Intents.ALL)

# Define the available RUs
ru_dict = {
    "illkirch": "illkirch",
    "cronenbourg": "cronenbourg",
    "paul-appell": "paul-appell"
}


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

    # Get the data from the API corresponding to the wanted RU
    ru = json_to_dict(get_html(env["URL_API"]+"/"+ru_dict[name.lower()]))

    # Get the date
    current_date = get_date()

    embed = interactions.Embed(title="Menu RU "+name,
                               description="__**"+format_date_to_french(current_date)+"**__"+"\n```yaml\n"+print_lunch_diner(current_date, ru)+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await ctx.send(embeds=embed)


@interactions.Task.create(interactions.TimeTrigger(hour=int(env["HOUR"]), minute=int(env["MINUTE"]), utc=False))
async def _daily_menu():

    # Don't print the menu on week-end
    if datetime.now().weekday() in [5, 6]:
        return

    # Get the date
    current_date = get_date()

    channel = await bot.fetch_channel(env["CHANNEL_ID"])
    await channel.purge(deletion_limit=10)
    embed = interactions.Embed(title="Menu RU Illkirch",
                               description="__**"+format_date_to_french(current_date)+"**__"+"\n```yaml\n"+print_lunch_diner(current_date, json_to_dict(get_html(env["URL_API"]+"/illkirch")))+"```", color=0x00ff00)
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
