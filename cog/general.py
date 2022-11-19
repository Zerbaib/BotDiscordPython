
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
class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ping")
    async def ping(self, context):
        """
        Vérifiez si le bot est en ligne et regarde la latence.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"La latence du bot est {round(self.bot.latency * 1000)}ms.",
            color=0xE8C02A
        )
        await context.send(embed=embed)
        
    @commands.command(name="server", aliases=["support", "supportserver"])
    async def server(self, context):
        """
        Obtenez le lien d'invitation du serveur discord du bot pour obtenir de l'aide.
        """
        embed = discord.Embed(
            description="Rejoignez le serveur de support du bot en cliquant sur [ici](https://discord.gg/XghGYjC6HF).",
            color=0xE8C02A,
        )

        try:
            await context.author.send(embed=embed)
            await context.send("Je vous ai envoyé un message privé !")
        except discord.Forbidden:
            await context.send(embed=embed)
            
    @commands.command(name="invite")
    async def invite(self, context):
        """
        Obtenez le lien d'invitation du bot pour pouvoir l'inviter.
        """
        embed = discord.Embed(
            description=f"Invitez-moi en cliquant [ici](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=8).",
            color=0xE8C02A
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Je vous ai envoyé un message privé!")
        except discord.Forbidden:
            await context.send(embed=embed)
            
    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Obtenez des informations utiles (ou non) sur le bot.
        """
        embed = discord.Embed(
            description="**PikaPika#4626**",
            color=0xE8C02A
        )
        embed.set_author(
            name="Informations sur le bot"
        )
        embed.add_field(
            name="Propriétaire:",
            value="Zerbaib#0001",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config['bot_prefix']}",
            inline=False
        )
        embed.add_field(name="Version du bot :", value="1.5", inline=True)
        embed.add_field(
            name="Version de Python :",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(name="Version de Discord.py :", value="1.7.3", inline=True)
        embed.set_footer(
            text=f"Demandé par {context.message.author}"
        )
        await context.send(embed=embed)
        
    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        """
        Obtenez des informations utiles (ou non) sur le serveur.
        """
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Nom du serveur:**",
            description=f"{server}",
            color=0xE8C02A
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Propriétaire",
            value=f"{server.owner}"#\n{server.owner.id}"
        )
        embed.add_field(
            name="Serveur ID",
            value=server.id
        )
        embed.add_field(
            name="Nombre de membres",
            value=server.member_count
        )
        embed.add_field(
            name="Canaux texte/vocaux",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Créé à: {time}"
        )
        await context.send(embed=embed)
            
    @commands.command(name="poll")
    async def poll(self, context, *, title):
        """
        Créez un sondage où les membres peuvent voter.
        """
        embed = discord.Embed(
            title="Un nouveau sondage a été créé!",
            description=f"{title}",
            color=0xE8C02A
        )
        embed.set_footer(
            text=f"Sondage créé par: {context.message.author} • Réagir pour voter!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")
#
 # # # Fin du block commandes

 # # # Ajout du cog au bot
#
def setup(bot):
    bot.add_cog(general(bot))
#
 # # # Fin de l'ajout
