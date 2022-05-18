import discord
from discord.ext import commands
#import discord_slash
import os
from json import load

#* intents
intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.guild_messages = True
intents.members = True
#* bots
bot = commands.Bot(command_prefix=">", help_command=None, intents=intents)
#slash = discord_slash.SlashCommand(bot, sync=True)



# on ready function
# Called when bot becomes live
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Minecraft"))
    total_cogs = len(os.listdir("cogs")) - 1
    loaded = 0
    for cog in os.listdir("cogs/"):
        if cog.endswith(".py"):
            bot.load_extension(f"cogs.{cog[:-3]}")
            loaded += 1

    print(f"logged in as {bot.user}, and loaded {loaded}/{total_cogs} cogs")

bot.run("OTM0MDE0NzQ1Nzc2ODgxNjY0.Yep7BA.1j0OYnjVniaezYYwAV_jT-WAFzU")