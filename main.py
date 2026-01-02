
import discord
from discord.ext import commands
import asyncio
from config import BOT_TOKEN, GUILD_ID

# Définition des Intents requis (nécessaire pour recevoir l'événement on_member_join)
intents = discord.Intents.default()
intents.members = True # Nécessaire pour on_member_join
intents.message_content = False # Pas besoin de lire le contenu des messages pour ces features

class CustomBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!', 
            intents=intents,
            help_command=None # Désactiver la commande help par défaut
        )
        # Liste des Cogs (fonctionnalités) à charger
        self.initial_extensions = [
            'cogs.welcome_handler',
            'cogs.admin_tools',
        ]

    async def setup_hook(self):
        """Chargement des Cogs et synchronisation des commandes."""
        print("INFO: Chargement des Cogs...")
        for extension in self.initial_extensions:
            await self.load_extension(extension)
            print(f"INFO: {extension} chargé.")
        
        # Synchronisation des commandes (pour le développement, on utilise l'ID du serveur)
        try:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"INFO: Commandes synchronisées : {len(synced)}")
        except Exception as e:
            print(f"ERREUR: Échec de la synchronisation des commandes : {e}")

    async def on_ready(self):
        """Appelé lorsque le bot est prêt."""
        print('--------------------------------------------------')
        print(f'BOT DÉMARRÉ - Connecté en tant que : {self.user.name}')
        print(f'ID : {self.user.id}')
        print('--------------------------------------------------')


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERREUR FATALE: Le token du bot n'a pas été trouvé. Assurez-vous d'avoir un fichier .env.")
    else:
        bot = CustomBot()
        bot.run(BOT_TOKEN)