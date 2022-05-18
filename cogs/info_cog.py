from discord import Embed, Color
from discord.ext import commands

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name="help")
    async def help(self, ctx):
        emb = Embed(title="bot commands", description="All bot commands", color=Color.from_rgb(255, 169, 99))
        emb.add_field(name="general commands", value="`help`\n`origin`\n`origins`\n`branches`\n`credits`")
        emb.add_field(name="branch commands", value="`register-branch`\n`add-origin`\n`delete-origin`")
        emb.add_field(name="Bot administator commands", value="`view-application`\n")
        emb.set_footer(text="Some commands have more info when you use `><command> help` example `>origin help`")

        await ctx.send(embed=emb)
    
    @commands.command(name="branch-info")
    async def branch_info(self, ctx):
        await ctx.send("check your dms")
        author = ctx.author

        await author.send("Branches are a new system being added in to allow addon makers to add their origins to the bot as well")
        await author.send("You can apply for a branch by sending `>register-branch` and can add or delete any origins you choose in your branch")

    
    @commands.command(name="credits")
    async def creditscom(self, ctx):
        emb = Embed(title="People who helped with this project", color=Color.from_rgb(255, 169, 99))
        emb.add_field(name="Programmers", value="`Karsonthefoxx#1260`")
        emb.add_field(name="Ideas", value="`lammas123#6714`")
        emb.add_field(name="early testers", value="`AR4™#6524`\n`frosty#5883`\n`AdamMC#5035`")
        emb.set_footer(text="VERSION=V1.3 Branch update", inline=False)

        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(info(bot))