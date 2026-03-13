import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche la liste des commandes du bot.")
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📘 Liste des commandes",
            description="Voici toutes les commandes disponibles sur le bot.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🛠️ Modération",
            value=(
                "**/clear** — Supprime des messages\n"
                "**/warn** — Avertit un membre\n"
                "**/mute** — Mute un membre\n"
                "**/unmute** — Unmute un membre\n"
                "**/ban** — Ban un membre\n"
                "**/unban** — Déban via ID\n"
                "**/lock** — Verrouille le salon\n"
                "**/unlock** — Déverrouille le salon\n"
                "**/slowmode** — Active un slowmode\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🧰 Utilitaires",
            value=(
                "**/ping** — Latence du bot\n"
                "**/userinfo** — Infos d’un membre\n"
                "**/serverinfo** — Infos du serveur\n"
                "**/avatar** — Avatar d’un membre\n"
            ),
            inline=False
        )

        embed.set_footer(text="wmx.dev — Bot de modération")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
