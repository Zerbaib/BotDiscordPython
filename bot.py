# Module
import json
import os
import platform
import random
import sys
import discord
import logging
from discord.ext import commands, tasks
from discord.ext.commands import Bot

# se connecte au fichier de config
if not os.path.isfile("config.json"):
    sys.exit("'config.json' pas trouvé! Veuillez l'ajouter et réessayer.")
else:
    with open("config.json") as file:
        config = json.load(file)

# variable
intents = discord.Intents.default()
bot = Bot(command_prefix=config["bot_prefix"], intents=intents)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
