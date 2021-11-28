
 # # # Block modules
#
import json
import os
import platform
import random
import sys
import aiohttp
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
class crypto(commands.Cog, name="crypto"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        """
        Obtenez le prix actuel du bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Le prix du Bitcoin est: ${response['bpi']['USD']['rate']}",
                color=0xE8C02A
            )
            await context.send(embed=embed)
#
 # # # Fin du block commandes

 # # # Ajout du cog au bot
#
def setup(bot):
    bot.add_cog(crypto(bot))
#
 # # # Fin de l'ajout
