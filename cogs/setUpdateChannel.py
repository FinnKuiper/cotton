import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
from pymongo_get_database import get_database

load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))


class SetUpdateChannel(commands.Cog):
    @commands.hybrid_command(
        name="setupdatechannel",
        with_app_command=True,
        description="Set the update channel for the bot",
    )
    @app_commands.guilds(discord.Object(id=guild_id))
    @commands.has_permissions(administrator=True)
    async def setupdatechannel(self, ctx, channel: discord.TextChannel):
        guild = ctx.guild
        # get database
        dbname = get_database()
        collection_name = dbname["guild"]

        channel = discord.utils.get(guild.text_channels, name=f"{channel}")

        channel_id = channel.id

        # check if guild is already in the system
        guild_data = collection_name.find_one({"guild_id": guild.id})
        if not guild_data:
            await ctx.send(
                f"{guild.name} is not in the setted up yet! Use the command `!setup` to add the guild to the system"
            )
            return

        # get current update channel
        update_channel_id = guild_data["update_channel"]
        update_channel = guild.get_channel(update_channel_id)

        # check if channel_id is none or not a numeric value
        if channel_id == None or not str(channel_id).isnumeric():
            if update_channel or None:
                await ctx.send(
                    f"The current update channel is {update_channel.mention}"
                )
                return
            else:
                await ctx.send("No update channel has been set yet")
                return
        else:
            # update update channel
            collection_name.update_one(
                {"guild_id": guild.id}, {
                    "$set": {"update_channel": int(channel_id)}}
            )
            await ctx.send(f"Channel changed to `{update_channel.mention}`")
            return

    @commands.Cog.listener()
    async def on_ready(self):
        print("Setup is ready")


async def setup(bot):
    await bot.add_cog(SetUpdateChannel(bot))
