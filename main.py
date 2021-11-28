
 # # # Block modules
#
import json
import os
import platform
import random
import sys
import discord
import logging
from discord.ext import commands, tasks
from discord.ext.commands import Bot
#
 # # # Fin du block modules

 # # # Block json
#
if not os.path.isfile("config.json"):
    sys.exit("ERROR: Le fichier 'config.json' n'a pas été trouvé !")
else:
    with open("config.json") as file:
        config = json.load(file)
#
 # # # Fin du block json

 # # # Block variable/intents
#
intents = discord.Intents.default()
bot = Bot(command_prefix=config["bot_prefix"], intents=intents)
bot.remove_command("help")

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#
 # # # Fin du block variable/intents

 # # # Block event
#
@bot.event
async def on_ready():
    print(f"connecté en tant que {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Run sur: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()

@tasks.loop(minutes=0.1)
async def status_task():
    statuses = [f"{config['bot_prefix']}help", "V.1.5", "V2 en dev ^^", "je soutiens: oz-projects.fr/", "je soutiens: eclazion.net", "tous pour Discord.py", "Dev by: Zerbaib", "prefix: +"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

if __name__ == "__main__":
    for file in os.listdir("./cog"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cog.{extension}")
                print(f"Extension chargée '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Échec du chargement de l'extension {extension}\n{exception}")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    with open("blacklist.json") as file:
        blacklist = json.load(file)
    if message.author.id in blacklist["ids"]:
        return
    await bot.process_commands(message)

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hé, s'il te plaît, ralentis !",
            description=f"Vous pouvez réutiliser cette commande dans {f'{round(hours)} heures' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} secondes' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="Il vous manque l'autorisation `" + ", ".join(
                error.missing_perms) + "` pour exécuter cette commande!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error
#
 # # # Fin du block event

 # # # Block token
#
bot.run(config["token"])
#
 # # # Fin du block token
