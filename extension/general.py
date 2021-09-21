
import json
import os
import platform
import random
import sys

import aiohttp
import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' pas trouvé! Veuillez l'ajouter et réessayer.")
else:
    with open("config.json") as file:
        config = json.load(file)


class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Obtenez des informations utiles (ou non) sur le bot.
        """
        embed = discord.Embed(
            description="PikaPika | InDev#4626",
            color=0x42F56C
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
            name="Version de Python :",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config['bot_prefix']}",
            inline=False
        )
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
            color=0x42F56C
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

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Vérifiez si le bot est vivant.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"La latence du bot est {round(self.bot.latency * 1000)}ms.",
            color=0x42F56C
        )
        await context.send(embed=embed)

    @commands.command(name="invite")
    async def invite(self, context):
        """
        Obtenez le lien d'invitation du bot pour pouvoir l'inviter.
        """
        embed = discord.Embed(
            description=f"Invitez-moi en cliquant [ici](https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&scope=bot&permissions=8).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Je vous ai envoyé un message privé!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.command(name="server", aliases=["support", "supportserver"])
    async def server(self, context):
        """
        Obtenez le lien d'invitation du serveur discord du bot pour obtenir de l'aide.
        """
        embed = discord.Embed(
            description=f"Rejoignez le serveur de support du bot en cliquant sur [ici](https://discord.gg/nWGWwPY84b).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Je vous ai envoyé un message privé!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.command(name="poll")
    async def poll(self, context, *, title):
        """
        Créez un sondage où les membres peuvent voter.
        """
        embed = discord.Embed(
            title="Un nouveau sondage a été créé!",
            description=f"{title}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"Sondage créé par: {context.message.author} • Réagir pour voter!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="8ball")
    async def eight_ball(self, context, *, question):
        """
        Posez n'importe quelle question au bot.
        """
        answers = ['Il est certain.', "C'est décidément ainsi.", 'Vous pouvez vous y fier.', 'Sans aucun doute.',
                   'Oui définitivement.', 'Comme je vois, oui.', 'Le plus probable.', 'Bonnes perspectives.', 'Oui.',
                   'Les signes pointent vers Oui.', 'Répondez brumeux, réessayez.', 'Demander à nouveau plus tard.', 'Mieux vaut ne pas vous le dire maintenant.',
                   'Impossible de prédire maintenant.', 'Concentrez-vous et redemandez plus tard.', 'Ne comptez pas dessus.', 'Ma réponse est non.',
                   'Mes sources disent non.', 'Les perspectives ne sont pas si bonnes.', 'Très douteux.']
        embed = discord.Embed(
            title="**Ma réponse:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x42F56C
        )
        embed.set_footer(
            text=f"La question était: {question}"
        )
        await context.send(embed=embed)

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
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=0x42F56C
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(general(bot))
