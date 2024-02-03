import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="poll",
        with_app_command=True,
        description="Create a poll",
        aliases=["p"],
        pass_context=True,
    )
    @app_commands.guilds(discord.Object(id=guild_id))
    async def poll(self, ctx, question, *options):

        print(options)
        if len(options) > 10:
            return await ctx.send("You can only have 10 options")
        if len(options) < 2:
            return await ctx.send("You need at least 2 options")

        embed = discord.Embed(
            title="Poll",
            description=question,
            color=discord.Color.blue(),
        )
        for i, option in enumerate(options):
            embed.add_field(name=f"Option {i+1}", value=option, inline=False)
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(chr(127462 + i))


async def setup(bot):
    await bot.add_cog(Poll(bot))
