
import json
import os
import sys

import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' pas trouvé! Veuillez l'ajouter et réessayer.")
else:
    with open("config.json") as file:
        config = json.load(file)


class moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason="Non précisé"):
        """
        Exclure un utilisateur du serveur.
        """
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="L'utilisateur a des autorisations d'administrateur.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="Utilisateur expulsé !",
                    description=f"**{member}** a été expulsé par **{context.message.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Raison:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"Vous avez été expulsé par **{context.message.author}**!\nRaison: {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="Une erreur s'est produite lors de la tentative de kick de l'utilisateur. Assurez-vous que mon rôle est au-dessus du rôle de l'utilisateur que vous souhaitez expulser.",
                    color=0xE02B2B
                )
                await context.message.channel.send(embed=embed)

    @commands.command(name="nick")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, context, member: discord.Member, *, nickname=None):
        """
        Changer le pseudo d'un utilisateur sur un serveur.
        """
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Pseudo modifié!",
                description=f"**{member}'s** le nouveau surnom est **{nickname}**!",
                color=0x42F56C
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="Une erreur s'est produite lors de la tentative de modification du pseudonyme de l'utilisateur. Assurez-vous que mon rôle est au-dessus du rôle de l'utilisateur dont vous souhaitez modifier le pseudo.",
                color=0xE02B2B
            )
            await context.message.channel.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason="Non précisé"):
        """
        Banni un utilisateur du serveur.
        """
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="L'utilisateur a des autorisations d'administrateur.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="Utilisateur banni!",
                    description=f"**{member}** a été banni par **{context.message.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Raison:",
                    value=reason
                )
                await context.send(embed=embed)
                await member.send(f"Vous avez été banni par **{context.message.author}**!\nRaison: {reason}")
        except:
            embed = discord.Embed(
                title="Error!",
                description="Une erreur s'est produite lors de la tentative de bannissement de l'utilisateur. Assurez-vous que mon rôle est au-dessus du rôle de l'utilisateur que vous souhaitez bannir.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, context, member: discord.Member, *, reason="Non précisé"):
        """
        Avertit un utilisateur dans ses messages privés.
        """
        embed = discord.Embed(
            title="Utilisateur averti!",
            description=f"**{member}** a été averti par **{context.message.author}**!",
            color=0x42F56C
        )
        embed.add_field(
            name="Raison:",
            value=reason
        )
        await context.send(embed=embed)
        try:
            await member.send(f"Vous avez été prévenu par **{context.message.author}**!\nRaison: {reason}")
        except:
            pass

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def purge(self, context, amount):
        """
        Supprimez un certain nombre de messages.
        """
        try:
            amount = int(amount)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` n'est pas un nombre valide.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` n'est pas un nombre valide.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        purged_messages = await context.message.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Chat effacé!",
            description=f"**{context.message.author}** effacé **{len(purged_messages)}** messages!",
            color=0x42F56C
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(moderation(bot))
