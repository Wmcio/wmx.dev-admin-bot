import discord
from discord.ext import commands
from discord import app_commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Affiche la latence du bot.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong ! {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="userinfo", description="Infos sur un membre.")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"Infos de {member}", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Compte créé", value=member.created_at.strftime("%d/%m/%Y"))
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Infos du serveur.")
    async def serverinfo(self, interaction: discord.Interaction):
        guild = interaction.guild
        embed = discord.Embed(title="Infos du serveur", color=discord.Color.green())
        embed.add_field(name="Nom", value=guild.name)
        embed.add_field(name="Membres", value=guild.member_count)
        embed.set_thumbnail(url=guild.icon)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Affiche l'avatar d'un membre.")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        await interaction.response.send_message(member.avatar)

async def setup(bot):
    await bot.add_cog(Utils(bot))
