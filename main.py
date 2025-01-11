from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineQueryResultArticle, InputTextMessageContent, InlineQuery, InlineQueryResult
from aiogram.filters import Command
import asyncio
import pyshorteners
import os 
import logging
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Бот запущен и работает...')


def shorten_url(url):
    try:
        return pyshorteners.Shortener().clckru.short(url)
    except Exception as e:
        return "Введите корректную ссылку"


@dp.message(Command('start'))
async def start(msg: Message):
    await msg.answer('Привет! Я бот для сокращения ссылок. Можешь использовать inline режим, чтобы сократить ссылку в любом чате\n\nЧтобы сократить ссылку введите: @dourlbot ссылка')

@dp.message()
async def short_link(msg: Message):
    url = msg.text
    result = shorten_url(url)
    print(result)
    if result == 'Введите корректную ссылку':
        await msg.answer(result)
    else:
        await msg.answer(f"Ваша ссылка: {result}")
    


@dp.inline_query()
async def process_inline(query: InlineQuery):
    query_text = query.query.strip()
    results = []
    result = shorten_url(query_text)
    if result != 'Введите корректную ссылку':
        results.append(
            InlineQueryResultArticle(
                id="short",
                title="Сократить",
                description="Сократите ссылку",
                input_message_content=InputTextMessageContent(
                    message_text=f"Ваша ссылка: {result}"
                )
            )
        )
    else:
        results.append(
                InlineQueryResultArticle(
                    id="error_fetch",
                    title="Ошибка",
                    description="Ссылка некорректна",
                    input_message_content=InputTextMessageContent(
                        message_text="Не удалось сократить. Проверьте ссылку"
                    ),
                )
            )
        
    await query.answer(results, cache_time=1, is_personal=True)    



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    
