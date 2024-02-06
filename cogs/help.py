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
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_author(
            name="Poeks",
            icon_url="https://cdn.discordapp.com/app-icons/868469587426045973/e42d5623fc11af69f6a84dbef205f3ef.png?size=256",
        )
        # add link to discord bot server
        embed.add_field(
            name="Support",
            value="[Discord Server](https://discord.gg/3m8T6JX)",
            inline=False,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
