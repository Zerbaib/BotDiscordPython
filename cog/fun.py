
 # # # Block modules
#
import asyncio
import json
import os
import random
import sys
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
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
class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot
        
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
                    embed = discord.Embed(description=data["text"], color=0xE8C02A)
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
        embed = discord.Embed(title="Choisissez s'il vous plaît", color=0xE8C02A)
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

            result_embed = discord.Embed(color=0xE8C02A)
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar_url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**C'est égalité!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0xE8C02A
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**Tu as gagné!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0xE8C02A
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**Tu as gagné!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0xE8C02A
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**Tu as gagné!**\nvous avez choisi {user_choice_emote} et j'ai choisi {bot_choice_emote}."
                result_embed.colour = 0xE8C02A
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
            color=0xE8C02A
        )
        embed.set_footer(
            text=f"La question était: {question}"
        )
        await context.send(embed=embed)
#
 # # # Fin du block commandes

 # # # Ajout du cog au bot
#
def setup(bot):
    bot.add_cog(Fun(bot))
#
 # # # Fin de l'ajout
