import discord
from discord.ext import commands
from discord import app_commands
import datetime

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    warnings = {}

    @app_commands.command(name="clear", description="Supprime un nombre de messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{amount} messages supprimés.", ephemeral=True)

    @app_commands.command(name="warn", description="Avertit un membre.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        uid = member.id
        self.warnings[uid] = self.warnings.get(uid, 0) + 1

        await interaction.response.send_message(
            f"{member.mention} a reçu un warn. Total : {self.warnings[uid]}"
        )

        if self.warnings[uid] >= 3:
            until = discord.utils.utcnow() + datetime.timedelta(minutes=5)
            await member.timeout(until=until, reason="3 warns")

    @app_commands.command(name="mute", description="Mute un membre.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int):
        until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
        await member.timeout(until=until)
        await interaction.response.send_message(f"{member.mention} mute {minutes} minutes.")

    @app_commands.command(name="unmute", description="Unmute un membre.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await member.timeout(None)
        await interaction.response.send_message(f"{member.mention} a été unmute.")

    @app_commands.command(name="ban", description="Ban un membre.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member} banni.")

    @app_commands.command(name="unban", description="Déban un utilisateur via son ID.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user} débanni.")

    @app_commands.command(name="lock", description="Verrouille le salon.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
        await interaction.response.send_message("Salon verrouillé.")

    @app_commands.command(name="unlock", description="Déverrouille le salon.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, interaction: discord.Interaction):
        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
        await interaction.response.send_message("Salon déverrouillé.")

    @app_commands.command(name="slowmode", description="Active un slowmode.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode(self, interaction: discord.Interaction, seconds: int):
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"Slowmode réglé sur {seconds}s.")

async def setup(bot):
    await bot.add_cog(Admin(bot))
