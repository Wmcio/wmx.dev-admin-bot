import discord
from discord.ext import commands
import re
import time
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_messages = {}

        self.BAD_WORDS = ["fdp", "ntm", "pute", "tg", "enculé", "merde"]
        self.link_regex = re.compile(r"https?://\S+|www\.\S+")
        self.flood_regex = re.compile(r"(.)\1{6,}")
        self.SPAM_LIMIT = 5
        self.SPAM_INTERVAL = 7
        self.SPAM_PUNISH = 10
        self.MAX_MENTIONS = 4

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()

        # Anti-lien
        if self.link_regex.search(content):
            await message.delete()
            return

        # Anti-insultes
        if any(w in content for w in self.BAD_WORDS):
            await message.delete()
            return

        # Anti-flood
        if self.flood_regex.search(content):
            await message.delete()
            return

        # Anti-mentions massives
        if len(message.mentions) > self.MAX_MENTIONS:
            await message.delete()
            return

        # Anti-spam
        now = time.time()
        uid = message.author.id

        if uid not in self.user_messages:
            self.user_messages[uid] = []

        self.user_messages[uid] = [t for t in self.user_messages[uid] if now - t < self.SPAM_INTERVAL]
        self.user_messages[uid].append(now)

        if len(self.user_messages[uid]) > self.SPAM_LIMIT:
            until = discord.utils.utcnow() + datetime.timedelta(seconds=self.SPAM_PUNISH)
            try:
                await message.author.timeout(until=until, reason="Spam")
            except:
                pass

async def setup(bot):
    await bot.add_cog(Moderation(bot))
