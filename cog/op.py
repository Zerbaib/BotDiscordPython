import json
import os
import platform
import random
import sys
import aiohttp
import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("ERROR: Le fichier 'config.json' n'a pas été trouvé !")
else:
    with open("config.json") as file:
        config = json.load(file)

class admin(commands.Cog, name="admin"):
    def __init__(self, bot):
    self.bot = bot

def setup(bot):
    bot.add_cog(admin(bot)):
