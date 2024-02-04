from discord.ext import commands
from dotenv import load_dotenv
import os
import discord

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        with_app_command=True,
        description="Get all the commands of the bot",
    )
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help",
            description="All the commands of the bot",
            color=0xEB34E5,
            timestamp=ctx.message.created_at,
        )
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        for command in self.bot.commands:
            embed.add_field(name=command.name, value=command.description, inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
