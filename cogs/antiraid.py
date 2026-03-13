import discord
from discord.ext import commands
import time

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.joins = []

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = time.time()
        self.joins = [t for t in self.joins if now - t < 10]
        self.joins.append(now)

        # Comptes récents
        account_age = (discord.utils.utcnow() - member.created_at).days
        if account_age < 7:
            try:
                await member.kick(reason="Compte trop récent (anti-raid)")
            except:
                pass

        # Arrivées massives
        if len(self.joins) >= 5:
            try:
                await member.guild.system_channel.send("⚠️ Détection d’un raid (arrivées massives).")
            except:
                pass

async def setup(bot):
    await bot.add_cog(AntiRaid(bot))
