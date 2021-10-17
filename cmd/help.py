# module
import json
import os
import sys
import discord
from discord.ext import commands

# json
if not os.path.isfile("config.json"):
    sys.exit("'config.json' Non trouver")
else:
    with open("config.json") as file:
        config = json.load(file)

# class
class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    # commande
    @commands.command(name="help")
    async def help(self, context):
        """
        Répertoriez toutes les commandes le bot a.
        """
        prefix = config["bot_prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="Liste des commandes disponibles :", color=0x42F56C)
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            command_list = [command.name for command in commands]
            command_description = [command.help for command in commands]
            help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
            embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)

# fonction
def setup(bot):
    bot.add_cog(Help(bot))
