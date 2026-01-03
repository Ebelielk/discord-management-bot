
import discord
from discord.ext import commands
from discord import app_commands, Guild
from config import GUILD_ID, ANNOUNCEMENT_COLOR
import investpy
from datetime import datetime, timedelta
import pandas as pd

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
    
    @app_commands.command(name="calendrier_economique", description="Envoie le calendrier économique hebdomadaire.")
    @app_commands.describe(
        salon="Le salon où envoyer le calendrier (par défaut: salon actuel)."
    )
    async def calendrier_economique_command(self, interaction: discord.Interaction, 
                                           salon: discord.TextChannel = None):
        
        target_channel = salon if salon else interaction.channel
        
        await interaction.response.defer()  # Pour les opérations longues
        
        try:
            # Obtenir la date actuelle et la date dans 7 jours
            today = datetime.now()
            next_week = today + timedelta(days=7)
            
            # Récupérer le calendrier économique
            calendar = investpy.economic_calendar(
                from_date=today.strftime('%d/%m/%Y'),
                to_date=next_week.strftime('%d/%m/%Y')
            )
            
            if calendar.empty:
                embed = discord.Embed(
                    title="📅 Calendrier Économique Hebdomadaire",
                    description="Aucun événement économique prévu cette semaine.",
                    color=ANNOUNCEMENT_COLOR,
                    timestamp=discord.utils.utcnow()
                )
            else:
                # Créer l'embed avec les événements
                embed = discord.Embed(
                    title="📅 Calendrier Économique Hebdomadaire",
                    description=f"Événements du {today.strftime('%d/%m/%Y')} au {next_week.strftime('%d/%m/%Y')}",
                    color=ANNOUNCEMENT_COLOR,
                    timestamp=discord.utils.utcnow()
                )
                
                # Grouper par date
                calendar['date'] = calendar['date'].dt.strftime('%d/%m/%Y')
                grouped = calendar.groupby('date')
                
                for date, events in grouped:
                    event_list = []
                    for _, event in events.iterrows():
                        time = event['time'] if pd.notna(event['time']) else "N/A"
                        currency = event['currency'] if pd.notna(event['currency']) else ""
                        event_name = event['event']
                        forecast = event['forecast'] if pd.notna(event['forecast']) else ""
                        previous = event['previous'] if pd.notna(event['previous']) else ""
                        
                        event_str = f"🕒 {time} - {currency} {event_name}"
                        if forecast:
                            event_str += f" (Prévision: {forecast})"
                        if previous:
                            event_str += f" (Précédent: {previous})"
                        
                        event_list.append(event_str)
                    
                    embed.add_field(
                        name=f"📆 {date}",
                        value="\n".join(event_list[:5]),  # Limiter à 5 événements par jour
                        inline=False
                    )
            
            embed.set_footer(text=f"Demandé par {interaction.user.display_name}")
            
            await target_channel.send(embed=embed)
            await interaction.followup.send(
                f"✅ Calendrier économique envoyé dans {target_channel.mention} !", 
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erreur lors de la récupération du calendrier économique : {e}", 
                ephemeral=True
            )

# Fonction d'installation requise par discord.py
async def setup(bot):
    await bot.add_cog(AdminTools(bot), guilds=[discord.Object(id=GUILD_ID)])