
from discord import Embed, Color
from discord.ext import commands
import json
import os

#* Looks through the branches in db/branchs and looks for a branch that has the same author id as the one writting a message
def check_owner(authorid):
    found = False
    branches = os.listdir("db/branches/")
    for branch in branches:
        if os.path.exists(f"db/branches/{branch}/origins.json"):
            with open(f"db/branches/{branch}/origins.json", "r") as branch_data:
                branch_data = json.load(branch_data)
            
            if int(branch_data["author_id"]) == authorid:
                found = True
                return branch_data, branch
            
            else:
                found = False
        
        if found == True:
            break
    
    if found == False:
        return None

def check(author):
    def inner(message):
        return message.author == author
    return inner

class manage_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="add-origin")
    async def add_origin(self, ctx):
        branch_data, branch = check_owner(ctx.author.id)
        if branch_data != None:
            emb = Embed(title="Formatting origins", description="This bot uses a specific way to see the different arguments of the origin", color=Color.red())
            emb.add_field(name="Order of data", value="Origin name;Origin description(use NONE if there is none);Origin Power 1 Name:Origin Power 1 description; Origin power 2 name:Orign power 2 description")
            emb.add_field(name="example", value="Example origin;This origin is an example origin to show how to format the addition to the origin;Good example:Because this example is so good the user will know how to use this command;Nerd:Because you know how to program you will have to live with being called a nerd your entire life")

            await ctx.send(embed=emb)
            await ctx.send("You have 300 seconds to complete this action")

            origin_data = await self.bot.wait_for("message", check=check(ctx.author), timeout=300)

            origin_data = origin_data.content

            origin_data_items = origin_data.split(";")
            origin_name = origin_data_items[0]
            origin_description = origin_data_items[1]
            origin_powers = origin_data_items[2:]
            origin_power_sorted = []

            for power in origin_powers:
                power_data = power.split(":")
                origin_power_sorted.append({"name":power_data[0], "description":power_data[1]})
            origin = {"name": origin_name, "description": origin_description, "powers":origin_power_sorted}
            branch_data["origins"].append(origin)
            with open(f"db/branches/{branch}/origins.json", "w") as new_data:
                json.dump(branch_data, new_data)
            
            await ctx.send("Origin added")


        else:
            await ctx.reply("You dont own a branch at the moment")
    
    @commands.command(name="delete-origin")
    async def delete_origin(self, ctx, *origin_to_delete):
        branch_data, branch = check_owner(ctx.author.id)
        origin_to_delete = " ".join(origin_to_delete)
        if branch_data != None:
            found = False
            for origin in branch_data["origins"]:

                if origin["name"].lower() == origin_to_delete.lower():
                    branch_data["origins"].remove(origin)
                    found = True

                    with open(f"db/branches/{branch}/origins.json", "w") as deleted_origin:
                        json.dump(branch_data, deleted_origin)
                    break
            
            if found == False:
                await ctx.send(f"The origin {origin_to_delete} was not found")
            
            else:
                await ctx.send("Origin removed")



def setup(bot):
    bot.add_cog(manage_cog(bot))