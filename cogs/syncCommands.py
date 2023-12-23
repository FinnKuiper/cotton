from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import discord

load_dotenv()
guild_id = os.getenv("GUILD_ID")
owner_id = os.getenv("OWNER_ID")


class SyncCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="synccommands", description="Sync slash commands")
    async def synccommands(self, ctx):
        # make sure the user is the owner of the bot
        if ctx.author.id != int(owner_id):
            await ctx.send("You are not the owner of the bot")
            return

        await ctx.send("Syncing commands...")
        await ctx.bot.tree.sync(guild=discord.Object(id=guild_id))
        await ctx.send("Synced commands!")


async def setup(bot):
    await bot.add_cog(SyncCommands(bot))
