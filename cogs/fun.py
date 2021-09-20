
import asyncio
import json
import os
import random
import sys

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import BucketType

if not os.path.isfile("config.json"):
    sys.exit("'config.json' pas trouvé! Veuillez l'ajouter et réessayer.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    """
    Why 1 and 86400?
    -> Because the user should be able to use the command *once* every *86400* seconds
    
    Why BucketType.user?
    -> Because the cool down only affects the current user, if you want other types of cool downs, here are they:
    - BucketType.default for a global basis.
    - BucketType.user for a per-user basis.
    - BucketType.server for a per-server basis.
    - BucketType.channel for a per-channel basis.
    """

    @commands.command(name="dailyfact")
    @commands.cooldown(1, 86400, BucketType.user)
    async def dailyfact(self, context):
        """
        Obtenez un fait quotidien, la commande ne peut être exécutée qu'une fois par jour par utilisateur.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                    await context.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="Il y a un problème avec l'API, veuillez réessayer plus tard",
                        color=0xE02B2B
                    )
                    await context.send(embed=embed)
                    self.dailyfact.reset_cooldown(context)

    @commands.command(name="pfc")
    async def rock_paper_scissors(self, context):
        """
        Joue a pierre, feuille et ciseaux contre le bot
        """
        choices = {
            0: "pierre",
            1: "feuille",
            2: "ciseaux"
        }
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }
        embed = discord.Embed(title="Choisissez s'il vous plaît", color=0xF59E42)
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = discord.Embed(color=0x42F56C)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**C'est un tirage!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0xF59E42
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**Tu as gagné!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**Tu as gagné!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**Tu as gagné!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0x42F56C
            else:
                result_embed.description = f"**J'ai gagné!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0xE02B2B
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = discord.Embed(title="Trop tard", color=0xE02B2B)
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.edit(embed=timeout_embed)


def setup(bot):
    bot.add_cog(Fun(bot))
