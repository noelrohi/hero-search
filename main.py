from modules import environ
import os
import disnake
from disnake.ext import commands


intents = disnake.Intents.default()  # All but the two privileged ones
intents.members = True  # Subscribe to the Members intent
intents.message_content = True
bot = commands.Bot(command_prefix=environ.prefix, intents=intents)

# get a list of all files in the "cogs" folder
cog_files = os.listdir("cogs")

# remove any files that don't end with ".py"
cog_files = [f for f in cog_files if f.endswith(".py")]

# loop through the list of files and load each one
for cog_file in cog_files:
    # remove the ".py" extension from the file name
    cog_name = cog_file[:-3]

    # load the cog
    bot.load_extension(f"cogs.{cog_name}")
    print((f"Loaded /cogs/{cog_name}.py"))

bot.run(environ.token)