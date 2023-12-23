# imports
import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from pymongo_get_database import get_database

# load environment variables
load_dotenv()
token = os.getenv("DISCORD_TOKEN")


async def get_prefix(bot, message):
    # get database
    dbname = get_database()
    collection_name = dbname["guild"]

    # get prefix
    guild_id = message.guild.id
    guild = collection_name.find_one({"guild_id": guild_id})
    prefix = guild["prefix"] if guild else "!"
    return prefix


# create bot
class Bot(commands.Bot):
    def __init__(
        self,
    ):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=get_prefix, intents=intents)

    async def on_command_error(self, ctx, error) -> None:
        await ctx.reply(error, ephemeral=True)

    # create bot and get the command prefix from the database


bot = Bot()


# load cogs
@bot.event
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            command = filename[:-3]
            await bot.load_extension(f"cogs.{command}")
            print(f"{command} loaded")
    print("Bot is ready")


# on added to guild add to mongo database
@bot.event
async def on_guild_join(guild):
    # get database
    dbname = get_database()
    collection_name = dbname["guild"]

    # create item
    item = {
        "name": guild.name,
        "guild_id": guild.id,
        "owner": guild.owner,
        "update_channel": None,
        "prefix": "!",
        "expiry_date": None,
    }

    # insert item
    collection_name.insert_one(item)
    print(f"Added {guild.name} to database")


# run bot
bot.run(token)
