from discord import Embed, Color
from discord.ext import commands
import os
import json

class veiw_origins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="origin")
    async def origin(self, ctx, *origin_data):
        if "".join(origin_data) == "help":
            emb = Embed(title=">origin help", description="Displays the powers of a specified origin.", color=Color.green())
            emb.add_field(name="Usage", value=">origin <origin name>;[Branch]")
            emb.add_field(name="example", value="`>origin example;karsonthefoxx`")
            emb.add_field(name="IMPORTANT!", value="if you are NOT trying to use an origin made by lammas123 then you need to specify a branch, This is the makers NAME not the addon name, use `branchs` to see all branches that are registered, use `>branch-info` for more information.")
            emb.set_footer(text="`[arg]` = optional, `<arg>` = required, DONT PUT THE BRACES!")
    
            await ctx.send(embed = emb)

        else:
            origin = " ".join(origin_data)
            origin = origin.split(";")
            if len(origin) == 1:
                origin.append("lammas123")
            
            origin_name = origin[0]
            branch_name = origin[1]
            found = False
            for branch in os.listdir("db/branches"):
                if branch.lower() == branch_name.lower():
                    found = True

                    with open(f"db/branches/{branch.lower()}/origins.json", "r") as branch_data:
                        branch_data = json.load(branch_data)
            
            if found == False:
                await ctx.send(f"Branch: {branch_name} was not found")
            
            else:
                found = False
                for origin in branch_data["origins"]:
                    if origin["name"].lower() == origin_name.lower():
                        found = True

                    emb = Embed(title=f"{origin_name.capitalize()} ({branch_name}/{origin_name})", description=origin["description"], color=Color.from_rgb(255, 169, 99))
                    
                    for power in origin["powers"]:
                        emb.add_field(name=power["name"], value=power["description"], inline=False)

                    await ctx.send(embed=emb)
                    break

    @commands.command(name="origins")
    async def origins(self, ctx, *branch):
        if " ".join(branch).lower() == "help":
            emb = Embed(title=">origins", description="Lists all origins in a branch", color=Color.green())
            emb.add_field(name="Usage", value=">origins <branch>")
            emb.add_field(name="example", value=">origins Karsonthefoxx")
            emb.set_footer(text="`<args>` = required, (DONT PUT BRACES)")

            await ctx.send(embed=emb)
        
        else:
            branch = " ".join(branch)

            if branch.lower() in os.listdir("db/branches"):
                with open(f"db/branches/{branch.lower()}/origins.json", "r") as branch_data:
                    branch_data = json.load(branch_data)
                
                branch_origins = []
                for origin in branch_data["origins"]:
                    branch_origins.append(origin["name"])
                
                formatted_origin_names = ""
                if len(branch_origins) != 0:
                    for origin in branch_origins:
                        formatted_origin_names += f"`{origin}`\n"
                else:
                    formatted_origin_names = "No origins added"

                emb = Embed(title=branch, description="origins in the branch", color=Color.from_rgb(255, 169, 99))
                emb.add_field(name="origins", value=formatted_origin_names)

                await ctx.send(embed=emb)
            
            else:
                await ctx.send(f"Branch: {branch} not found")

    @commands.command(name="branches")
    async def branches(self, ctx, *branch):
        emb = Embed(title="all branches", description="All currently added branches", color=Color.from_rgb(255, 169, 99))
        branches = ""
        for branch in os.listdir("db/branches/"):
            branches += f"`{branch}`\n"

        emb.add_field(name="branches", value=branches)
        await ctx.send(embed = emb)


def setup(bot):
    bot.add_cog(veiw_origins(bot))