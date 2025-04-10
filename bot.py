import asyncio
import logging
from datetime import datetime, timedelta
from telethon import TelegramClient, functions, types
from telethon.errors import FloodWaitError
from telethon.tl.functions.contacts import GetContactsRequest
from like_storage import load_like_storage, save_like_storage

async def run_bot(api_id: int, api_hash: str, session_name: str = "story_session"):
    logging.info("Запуск клиента...")
    client = TelegramClient(session_name, api_id, api_hash)
    likes = load_like_storage()

    async with client:
        contacts_response = await client(GetContactsRequest(hash=0))
        contacts = contacts_response.users

        for contact in contacts:
            logging.info(f'Проверка историй у контакта: {contact.first_name}')

            try:
                stories = await client(functions.stories.GetPeerStoriesRequest(
                    peer=types.InputPeerUser(contact.id, contact.access_hash))
                )
            except FloodWaitError as e:
                logging.warning(f'FloodWait: спим {e.seconds} секунд...')
                await asyncio.sleep(e.seconds)
                continue
            except Exception as e:
                logging.error(f'Ошибка при получении сторис: {e}')
                continue

            user_stories = stories.stories.stories

            if not user_stories:
                logging.info(f'Нет доступных сторис у контакта: {contact.first_name}')
                continue

            first_story = user_stories[0]
            last_like = likes.get(str(contact.id))

            if not last_like or datetime.now() - datetime.fromisoformat(last_like) > timedelta(days=3):
                try:
                    await client(functions.stories.SendReactionRequest(
                        peer=types.InputPeerUser(contact.id, contact.access_hash),
                        story_id=first_story.id,
                        reaction=types.ReactionEmoji(emoticon='👍')
                    ))
                    logging.info(f'Поставлен лайк контакту: {contact.first_name}')
                    likes[str(contact.id)] = datetime.now().isoformat()
                    save_like_storage(likes)
                except Exception as e:
                    logging.error(f'Ошибка при попытке поставить лайк: {e}')
            else:
                logging.info(f'Лайк недавно уже ставился контакту: {contact.first_name}')

            try:
                max_id = max(story.id for story in user_stories)
                await client(functions.stories.ReadStoriesRequest(
                    peer=types.InputPeerUser(contact.id, contact.access_hash),
                    max_id=max_id
                ))
                logging.info(f'Просмотрены все сторис у контакта: {contact.first_name}')
            except Exception as e:
                logging.error(f'Ошибка при просмотре сторис: {e}')

            await asyncio.sleep(3)
