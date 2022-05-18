from discord.ext import commands
from discord import Color, Embed
from json import dump, load
import os


class register_cog_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="register-branch", description="Register a new branch of the origins mod")
    @commands.cooldown(rate=1, per=604800, type=commands.BucketType.user)
    async def register_branch(self, ctx):
        def check(author):
            def inner(message):
                return message.author == author
            return inner


        await ctx.send("Setup init\n Would you like to clear messages? (y/n) (timeout=15S)")
        clear_messages = await self.bot.wait_for("message", check=check(ctx.author), timeout=15)
        if clear_messages.content.lower() == "y":
            clear_messages = True
        else:
            clear_messages = False

        bot_message = await ctx.send("What is the name of your addon? (use plain text) (timeout=60S)")

        name = await self.bot.wait_for("message", check=check(ctx.author), timeout=60)

        if clear_messages:
            await bot_message.delete()
            await name.delete()

        bot_message = await ctx.send("Discribe your pack. (must be at least 10 characters long excluding spaces) (timeout=120S)")
        description = await self.bot.wait_for("message", check=check(ctx.author), timeout=120)

        check_message = description.content.replace(" ", "")
        if len(check_message) >= 10:

            if clear_messages:
                await description.delete()
                await bot_message.delete()

            bot_message = await ctx.send("Add a download link to your addon here (timeout=200)")
            pack_download = await self.bot.wait_for("message", check=check(ctx.author), timeout=200)


            emb = Embed(title="Application pending", description="Your application may be pending for up to 1 week, if you do not receive a response you may re-apply", color=Color.from_rgb(0, 180, 0))
            await ctx.send(embed=emb)

            id_number = len(os.listdir("db/applications")) + 1
            
            file_name = f"application_{id_number}.json"
            

            request = {"author": ctx.author.name, "user_id": ctx.author.id, "pack_name": name.content.lower(), "description": description.content.lower(), "download": pack_download.content}
            with open(f"db/applications/{file_name}", "w") as new_application:
                dump(request, new_application)

        else:
            await ctx.send("Pack description not valid as it is too short, you can try again after 1 week")


def setup(bot):
    bot.add_cog(register_cog_command(bot))       