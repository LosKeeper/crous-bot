import interactions

from config import TOKEN
from html_parse import *

bot = interactions.Client(token=TOKEN,
                          intents=interactions.Intents.ALL)


@bot.command(name='menu', description='Print today\'s menu',)
async def _today(ctx: interactions.CommandContext):
    embed = interactions.Embed(title="**__Today Menu :__**",
                               description="```yaml\n"+parse_html(get_html())+"```", color=0x00ff00)
    embed.set_footer(text="By Thomas DUMOND",
                     icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    await ctx.send(embeds=embed)


# @ bot.event
# async def on_start():
    # # When bot is ready send time schedule in each 3 channels
    # # 2ARIO
    # channel = await bot._http.get_channel(CHANNEL_ID_2A_RIO)
    # channel = interactions.Channel(**channel, _client=bot._http)
    # await channel.purge(amount=10)
    # embed = interactions.Embed(title="Next lessons",
    #                            description=day_events(1, "2ARIO"),
    #                            color=0x00ff00)
    # embed.set_footer(text="By Thomas DUMOND",
    #                  icon_url="https://avatars.githubusercontent.com/u/28956167?s=400&u=195ab629066c0d1f29d6917d6479e59861349b2d&v=4")
    # await channel.send(embeds=embed)


bot.start()
