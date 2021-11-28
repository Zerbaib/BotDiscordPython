
 # # # Block modules
#
import json
import os
import sys
import discord
from discord.ext import commands
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

 # # # Block Commandes
#
class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context):
        """
        Répertoriez toutes les commandes le bot a.
        """
        prefix = config["bot_prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="Liste des commandes disponibles :", color=0xE8C02A)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            command_list = [command.name for command in commands]
            command_description = [command.help for command in commands]
            help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
            embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)
#
 # # # Fin du block commandes

 # # # Ajout du cog au bot
#
def setup(bot):
    bot.add_cog(Help(bot))
#
 # # # Fin de l'ajout
