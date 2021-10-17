# module
import json
import os
import platform
import random
import sys
import logging
import discord
from discord.ext import tasks
from discord.ext.commands import Bot

# json
if not os.path.isfile("config.json"):
    sys.exit("'config.json' Non trouver")
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

# event
@bot.event
async def on_ready():
    print("####################")
    print(f">>>> Connecter a {bot.user.name}")
    print(f">>> Discord.py API version: {discord.__version__}")
    print(f">> Python version: {platform.python_version()}")
    print(f"> Tourne sur: {platform.system()} {platform.release()} ({os.name})")
    print("####################")
    status_task.start()
    
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = [f"{config['bot_prefix']}help", "V.1", "je soutiens: oz-projects.fr/", "je soutiens: eclazion.net", "tous pour Discord.py", "Dev by: Zerbaib", "prefix: +", "V.2 bientot"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

# charger les commande (exentention
if __name__ == "__main__":
    for file in os.listdir("./cmd"):
        if file.endswith(".py"):
            extension = file[:-3]
            print("####################")
            try:
                bot.load_extension(f"cmd.{extension}")
                print(f"> extension charger'{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"> ECHEC sur {extension}\n{exception}")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    with open("blacklist.json") as file:
        blacklist = json.load(file)
    if message.author.id in blacklist["ids"]:
        return
    await bot.process_commands(message)

@bot.event # lence l'event
async def on_message(ctx): # l'envent on_message pour avoir tout les message
    # fait les variable pour les log avec la data
    serveur = ctx.guild.name # marche
    user = ctx.author # marche pas
    msg = ctx.content # marche pas
    # fait print les data recolter dans la cmd pour log les messages
    print(">>> serveur: " + serveur) # marche
#    print(">> user: " + user) # marche pas
#    print("> message:  " + msg) # marche pas
    print("####################")

@bot.event
async def on_command_error(context, error):
    raise error

# retire le help de base
bot.remove_command("help")

# token pour conneter a discord
bot.run(config["token"])
