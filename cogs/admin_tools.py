
import discord
from discord.ext import commands
from discord import app_commands, Guild
from config import GUILD_ID, ANNOUNCEMENT_COLOR

class AdminTools(commands.Cog):
    """
    Outils pour l'administration du serveur, incluant des commandes d'annonce 
    structurées (Embeds) restreintes aux administrateurs.
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # Restreint cette commande uniquement aux utilisateurs ayant la permission 'administrator'
    @app_commands.command(name="annonce", description="Crée un message d'annonce structuré (Embed).")
    @app_commands.describe(
        titre="Le titre principal de l'annonce.",
        contenu="Le corps du message d'annonce.",
        salon="Le salon où envoyer l'annonce (par défaut: salon actuel).",
        couleur_hexa="Couleur de la barre latérale (ex: #FF0000). Utilise la couleur par défaut si non spécifié."
    )
    #@app_commands.default_permissions(administrator=True)
    async def annonce_command(self, interaction: discord.Interaction, 
                             titre: str, 
                             contenu: str, 
                             salon: discord.TextChannel = None,
                             couleur_hexa: str = None):
        
        # Vérifie si le salon par défaut est le salon actuel si aucun n'est spécifié
        target_channel = salon if salon else interaction.channel

        # Gestion de la couleur (Sécurité et Clarté)
        try:
            if couleur_hexa and couleur_hexa.startswith('#') and len(couleur_hexa) == 7:
                # Convertit le code hexadécimal en entier
                color_int = int(couleur_hexa[1:], 16)
            else:
                color_int = ANNOUNCEMENT_COLOR
        except ValueError:
            # En cas d'erreur de conversion, utilise la couleur par défaut
            color_int = ANNOUNCEMENT_COLOR
            await interaction.response.send_message(
                "⚠️ Format de couleur invalide. Utilisation de la couleur par défaut.", 
                ephemeral=True
            )

        # Création de l'Embed
        embed = discord.Embed(
            title=titre,
            description=contenu,
            color=color_int,
            timestamp=discord.utils.utcnow() # Utilisation de l'heure du serveur Discord
        )
        embed.set_footer(text=f"Annonce par {interaction.user.display_name}")
        
        try:
            await target_channel.send(embed=embed)
            # Répondre à l'administrateur de manière éphémère (visible par lui seul)
            await interaction.response.send_message(
                f"✅ Annonce publiée dans {target_channel.mention} !", 
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Je n'ai pas la permission d'écrire dans ce salon.", 
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Une erreur s'est produite lors de l'envoi de l'annonce : {e}", 
                ephemeral=True
            )

# Fonction d'installation requise par discord.py
async def setup(bot):
    await bot.add_cog(AdminTools(bot), guilds=[discord.Object(id=GUILD_ID)])