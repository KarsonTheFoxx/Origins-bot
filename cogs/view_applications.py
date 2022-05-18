from discord.ext import commands
from discord import Color, Embed
import os
import json
class veiw_applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.moderator_ids = [394347954900697108, 855948446540496896]

    #* applications are stored in a json file under db/applications this cog allows the admins to verify others versions of the addon
    @commands.command(name="view-applications")
    @commands.cooldown(rate=5, per=20, type=commands.BucketType.channel)
    async def view_applications(self, ctx, id=None):
        # Checks if the author is a moderator
        if ctx.author.id in self.moderator_ids:
            def check(author):
                def inner(message):
                    return message.author == author
                return inner

            # Looks into the applications folder for applications
            for application in os.listdir("db/applications"):
                print(application)
                with open(f"db/applications/{application}", "r") as application_file:
                    application_data = json.load(application_file)
                # creates an embed to send
                emb = Embed(title=application_data["pack_name"], description=application_data["description"], color=Color.orange())
                emb.add_field(name="download", value=application_data["download"])
                emb.set_author(name=application_data["author"])
                emb.set_footer(text=application_data["user_id"])

                #sends the above embed and waits to see if the application is accepted or not
                await ctx.send(embed=emb)
                await ctx.send("Y/N (timeout=500)")
                approved = await self.bot.wait_for("message",check = check(ctx.author), timeout=500)
                user = self.bot.get_user(id=int(application_data["user_id"]))
                if approved.content.lower() == "y":

                    await user.send(f"Your pack has been approved by {ctx.author}")
                    new_branch_data = {"branch_owner": application_data["author"], "branch_name": application_data["pack_name"], "author_id": application_data["user_id"], "description":application_data["description"], "origins": []}
                    os.makedirs(f"db/branches/{application_data['author'].lower()}")
                    os.makedirs(f"db/branches/{application_data['author']}/res")
                    os.remove(f"db/applications/{application}")
                    with open(f"db/branches/{application_data['author'].lower()}/origins.json", "w") as branch:
                        json.dump(new_branch_data, branch)

                else:
                    await ctx.send("why are you denying the application? (timeout=100)")
                    reason = await self.bot.wait_for("message", check=check(ctx.author), timeout=100)

                    await user.send(f"Your pack has been denied by {ctx.author} for the following reason {reason.content}")
                    os.remove(f"db/applications/{application}")

        else:
            await ctx.send("You arent allowed to do this")

def setup(bot):
    bot.add_cog(veiw_applications(bot))                   