import valorant_api as val
import resource
import discord
import os
import traceback
from datetime import datetime

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = discord.Client()  #Creates Client
bot = commands.Bot(command_prefix='-')  #Sets prefix for commands(!Command)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def hello(ctx, user=None):
    try:
        if user is None:
            user = ctx.author
        elif user.isdigit():
            user = await bot.fetch_user(user)
        else:
            user = await bot.fetch_user(user.strip("<!@>"))
        await ctx.send('Hello ' + str(user))
        print('hello printed')

    except Exception:
        print(traceback.format_exc())


@bot.command()
async def mmr(ctx, username: str = "", tag: str = ""):
    try:
        if username == "help" or username == "":
            await ctx.send(
                '-mmr [Username] [Tag] *Do not add spaces to your username*')
        elif tag == "":
            await ctx.send(
                'Tag cannot be empty, please follow the following format \n -mmr [Username] [Tag] *Do not add spaces to your username*'
            )
        else:
            stats = await val.get_rank(username, tag)
            embed = discord.Embed(title=stats["name"] + '#' + tag.upper(),
                                  timestamp=datetime.utcnow())

            rank = stats["currenttierpatched"]
            rankNumber = resource.ranks[str(rank)]

            rankIconUrl = f"https://trackercdn.com/cdn/tracker.gg/valorant/icons/tiers/{rankNumber}.png"

            embed.set_thumbnail(url=rankIconUrl)

            embed.add_field(name="Current rank",
                            value=stats["currenttierpatched"])
            embed.add_field(name="Current RR", value=stats["ranking_in_tier"])
            embed.add_field(name="MMR", value=stats["elo"])
            embed.add_field(name="Change from last game",
                            value=stats["mmr_change_to_last_game"])

            await ctx.send(embed=embed)

        print('stats printed')

    except Exception:
        print(traceback.format_exc())
        await ctx.send('Player not ranked')


if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'))
