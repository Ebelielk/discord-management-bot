import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

# --- Configurations requises ---

BOT_TOKEN = os.getenv("DISCORD_TOKEN")

# ID du salon où les messages de bienvenue doivent être envoyés

WELCOME_CHANNEL_ID = 1421039341903282216  # <<< REMPLACER CECI PAR L'ID DU SALON

# ID de votre serveur (utile pour enregistrer rapidement les Slash Commands)

GUILD_ID = 1358775852250435674  # <<< REMPLACER CECI PAR L'ID DU SERVEUR

# --- Constantes pour les messages ---

WELCOME_MESSAGE_TEMPLATE = (
    "Salut {member.mention} ! Bienvenue sur notre serveur. "
    "N'hésite pas à consulter les règles et à te présenter."
)

# Couleur standard pour les Embeds d'annonce 
ANNOUNCEMENT_COLOR = 0x3498DB