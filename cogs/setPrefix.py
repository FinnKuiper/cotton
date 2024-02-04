from discord.ext import commands
from dotenv import load_dotenv
import os
from pymongo_get_database import get_database

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="setprefix",
        with_app_command=True,
        description="Set the prefix for the bot",
    )
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context, prefix: str = None):
        guild = ctx.guild
        # get database
        dbname = get_database()
        collection_name = dbname["guild"]

        # check if guild is already in the system
        guild_data = collection_name.find_one({"guild_id": guild.id})
        if not guild_data:
            await ctx.send(
                f"{guild.name} is not in the setted up yet! Use the command `!setup` to add the guild to the system"
            )
            return

        # get prefix
        oldPrefix = guild_data["prefix"]

        if prefix == None:
            await ctx.send(f"The current prefix is `{oldPrefix}`")
            return
        else:
            if len(prefix) > 1:
                await ctx.send("The prefix can only be one character long")
                return
            # update prefix
            collection_name.update_one(
                {"guild_id": guild.id}, {"$set": {"prefix": prefix}}
            )
            await ctx.send(f"Prefix changed to `{prefix}`")
            return

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setup is ready")


async def setup(bot):
    await bot.add_cog(SetPrefix(bot))
