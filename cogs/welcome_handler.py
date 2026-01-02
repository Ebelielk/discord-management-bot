import discord
from discord.ext import commands
import json
import os
from config import WELCOME_CHANNEL_ID, WELCOME_MESSAGE_TEMPLATE

# Nom du fichier pour stocker l'ID du message précédent
MSG_ID_FILE = "last_welcome_msg.json"

class WelcomeHandler(commands.Cog):
    """
    Gère la logique d'accueil des nouveaux membres, y compris la suppression 
    du message d'accueil précédent (logique de message volatile).
    """
    def __init__(self, bot):
        self.bot = bot
        self.last_msg_id = self._load_last_msg_id()
    
    def _load_last_msg_id(self):
        """Charge l'ID du dernier message depuis le fichier (Réduit l'obscurité)."""
        if os.path.exists(MSG_ID_FILE):
            with open(MSG_ID_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    # Assure que nous récupérons l'ID du message ou 0 si le fichier est vide
                    return data.get('last_id', 0)
                except json.JSONDecodeError:
                    return 0
        return 0

    def _save_last_msg_id(self, msg_id: int):
        """Sauvegarde l'ID du dernier message dans un fichier (Gestion de l'état)."""
        with open(MSG_ID_FILE, 'w') as f:
            json.dump({'last_id': msg_id}, f)

    async def _delete_previous_message(self, channel):
        """Tente de supprimer le message de bienvenue stocké précédemment."""
        if self.last_msg_id != 0:
            try:
                # Tente de récupérer le message
                msg = await channel.fetch_message(self.last_msg_id)
                await msg.delete()
                print(f"DEBUG: Message de bienvenue précédent (ID: {self.last_msg_id}) supprimé.")
            except discord.NotFound:
                # Le message a déjà été supprimé ou est trop vieux
                print("DEBUG: Message de bienvenue précédent non trouvé ou déjà supprimé.")
            except discord.Forbidden:
                print("ERREUR: Le bot n'a pas la permission de supprimer des messages.")
            except Exception as e:
                print(f"ERREUR lors de la suppression du message précédent : {e}")
        
        # Réinitialise l'ID après tentative de suppression
        self.last_msg_id = 0
        self._save_last_msg_id(0)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Événement déclenché à l'arrivée d'un nouveau membre."""
        
        # Récupère le salon configuré
        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel is None:
            print(f"ERREUR: Salon d'accueil ID {WELCOME_CHANNEL_ID} non trouvé.")
            return

        # 1. Suppression du message précédent
        await self._delete_previous_message(channel)
        
        # 2. Envoi du nouveau message de bienvenue
        welcome_text = WELCOME_MESSAGE_TEMPLATE.format(member=member)
        new_msg = await channel.send(welcome_text)
        
        # 3. Sauvegarde de l'ID du nouveau message
        self.last_msg_id = new_msg.id
        self._save_last_msg_id(new_msg.id)
        print(f"DEBUG: Nouveau message de bienvenue envoyé et ID stocké : {new_msg.id}")

# Fonction d'installation requise par discord.py
async def setup(bot):
    await bot.add_cog(WelcomeHandler(bot))