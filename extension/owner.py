
import json
import os
import sys

import discord
from discord.ext import commands

from helpers import json_manager

if not os.path.isfile("config.json"):
    sys.exit("'config.json' pas trouvé! Veuillez l'ajouter et réessayer.")
else:
    with open("config.json") as file:
        config = json.load(file)


class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    async def shutdown(self, context):
        """
        Arrêtez le bot
        """
        if context.message.author.id in config["owners"]:
            embed = discord.Embed(
                description="Au revoir! :wave:",
                color=0x42F56C
            )
            await context.send(embed=embed)
            await self.bot.close()
        else:
            embed = discord.Embed(
                title="Error!",
                description="Vous n'êtes pas autorisé à utiliser cette commande.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.command(name="say", aliases=["echo"])
    async def say(self, context, *, args):
        """
        Le bot dira tout ce que vous voulez.
        """
        if context.message.author.id in config["owners"]:
            await context.send(args)
        else:
            embed = discord.Embed(
                title="Error!",
                description="Vous n'êtes pas autorisé à utiliser cette commande.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        Le bot dira tout ce que vous voulez, mais dans les intégrations.
        """
        if context.message.author.id in config["owners"]:
            embed = discord.Embed(
                description=args,
                color=0x42F56C
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="Vous n'êtes pas autorisé à utiliser cette commande.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.group(name="blacklist")
    async def blacklist(self, context):
        """
        Vous permet d'ajouter ou de supprimer un utilisateur de ne pas pouvoir utiliser le bot.
        """
        if context.invoked_subcommand is None:
            with open("blacklist.json") as file:
                blacklist = json.load(file)
            embed = discord.Embed(
                title=f"Il y a actuellement {len(blacklist['ids'])} IDs sur liste noire",
                description=f"{', '.join(str(id) for id in blacklist['ids'])}",
                color=0x0000FF
            )
            await context.send(embed=embed)

    @blacklist.command(name="add")
    async def blacklist_add(self, context, member: discord.Member = None):
        """
        Vous permet d'ajouter un utilisateur de ne pas pouvoir utiliser le bot.
        """
        if context.message.author.id in config["owners"]:
            userID = member.id
            try:
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                if (userID in blacklist['ids']):
                    embed = discord.Embed(
                        title="Error!",
                        description=f"**{member.name}** est déjà dans la liste noire.",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    return
                json_manager.add_user_to_blacklist(userID)
                embed = discord.Embed(
                    title="Utilisateur sur liste noire",
                    description=f"**{member.name}** a été ajouté avec succès à la liste noire",
                    color=0x42F56C
                )
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                embed.set_footer(
                    text=f"Il y a maintenant {len(blacklist['ids'])} utilisateurs dans la liste noire"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"Une erreur inconnue s'est produite lors de la tentative d'ajout **{member.name}** à la liste noire.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="Vous n'êtes pas autorisé à utiliser cette commande.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @blacklist.command(name="remove")
    async def blacklist_remove(self, context, member: discord.Member = None):
        """
        Vous permet de supprimer un utilisateur de ne pas pouvoir utiliser le bot.
        """
        if context.message.author.id in config["owners"]:
            userID = member.id
            try:
                json_manager.remove_user_from_blacklist(userID)
                embed = discord.Embed(
                    title="Utilisateur supprimé de la liste noire",
                    description=f"**{member.name}** a été supprimé avec succès de la liste noire",
                    color=0x42F56C
                )
                with open("blacklist.json") as file:
                    blacklist = json.load(file)
                embed.set_footer(
                    text=f"Il y a maintenant {len(blacklist['ids'])} utilisateurs dans la liste noire"
                )
                await context.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Error!",
                    description=f"**{member.name}** n'est pas dans la liste noire.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="Vous n'êtes pas autorisé à utiliser cette commande.",
                color=0xE02B2B
            )
            await context.send(embed=embed)


def setup(bot):
    bot.add_cog(owner(bot))
