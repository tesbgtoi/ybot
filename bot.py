import logging
from telegram import Bot
from telegram.error import TelegramError

# Configurez le logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Informations spécifiques
TOKEN = "TOKEN_DU_BOT"
GROUP_ID = 123456789  # Remplacez par l'ID de votre groupe

# Fonction pour récupérer les demandes d'adhésion en attente
async def get_membership_requests(bot: Bot, group_id: int) -> list:
    try:
        administrators = await bot.get_chat_administrators(chat_id=group_id)
        membership_requests = []
        for admin in administrators:
            if not admin.user.is_bot:
                member = await bot.get_chat_member(chat_id=group_id, user_id=admin.user.id)
                if member.status == 'restricted':
                    membership_requests.append(member)
        return membership_requests
    except TelegramError as e:
        logger.error(f"Erreur lors de la récupération des demandes d'adhésion : {e}")
        return []

# Fonction pour envoyer des messages aux utilisateurs en attente
async def send_membership_notifications(bot: Bot, group_id: int, membership_requests: list) -> None:
    for request in membership_requests:
        try:
            await bot.send_message(
                chat_id=request.user.id,
                text="Votre demande d'adhésion au groupe a été reçue. Veuillez patienter pendant que l'administrateur approuve votre demande."
            )
            logger.info(f"Notification envoyée à l'utilisateur : {request.user.id}")
        except TelegramError as e:
            logger.error(f"Erreur lors de l'envoi de la notification à l'utilisateur {request.user.id} : {e}")

async def main() -> None:
    bot = Bot(token=TOKEN)

    # Récupérer les demandes d'adhésion en attente
    membership_requests = await get_membership_requests(bot, GROUP_ID)

    # Envoyer des messages aux utilisateurs en attente
    await send_membership_notifications(bot, GROUP_ID, membership_requests)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
