import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# ID du salon où envoyer le tableau
COMMANDS_CHANNEL_ID = 1482134036863258744

# Tableau des commandes
COMMANDS_TABLE = """
| Commande     | Paramètres                     | Description                                      |
|--------------|--------------------------------|--------------------------------------------------|
| /clear       | amount (nombre)                | Supprime un nombre de messages dans le salon.    |
| /warn        | member • reason                | Donne un avertissement (3 warns = mute 5 min).   |
| /mute        | member • minutes               | Mute un membre pour X minutes.                   |
| /unmute      | member                         | Retire le mute d’un membre.                      |
| /ban         | member • reason                | Bannit un membre du serveur.                     |
| /unban       | user_id                        | Débannit un utilisateur via son ID.              |
| /lock        | aucun                          | Verrouille le salon.                             |
| /unlock      | aucun                          | Déverrouille le salon.                           |
| /slowmode    | seconds                        | Active un slowmode sur le salon.                 |
| /ping        | aucun                          | Affiche la latence du bot.                       |
| /userinfo    | member (optionnel)             | Affiche les infos d’un membre.                   |
| /serverinfo  | aucun                          | Affiche les infos du serveur.                    |
| /avatar      | member (optionnel)             | Affiche l’avatar d’un membre.                    |
"""

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commandes slash synchronisées.")
    except Exception as e:
        print(e)

    # Envoi du tableau dans le salon choisi
    channel = bot.get_channel(COMMANDS_CHANNEL_ID)
    if channel:
        await channel.send("📘 **Commandes des #admins :**")
        await channel.send(f"```\n{COMMANDS_TABLE}\n```")

async def load_cogs():
    cogs = ["moderation", "admin", "antiraid", "utils", "help"]
    for cog in cogs:
        await bot.load_extension(f"cogs.{cog}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(os.getenv("DISCORD_TOKEN"))

asyncio.run(main())
