"""
Точка входа в бот-анкету
main.py оздает объект бота, диспетчер (Dispatcher), подключает роутер с обработчиками,
запускает pooling(от ссам опрашивает телеграмм-сервер и забирает новые события)
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import get_settings
from handlers import get_routers


async def main():
    """ Создает все основные объекты аiofram и запускает бота"""
    # загружаем настройки (токен бота)
    settings = get_settings()

    # bot - объект через который программа отправляет запросы в Telegram API.
    """
1. token=settings.bot_token — это секретный паспорт ботаТокен (token) — это длинная строчка из букв и цифр, 
    которую выдал главный бот в Телеграме (@BotFather).Зачем он нужен? Это уникальный ключ доступа. 
    Когда код пытается отправить сообщение пользователю, Телеграм спрашивает: «А ты вообще кто такой?». 
    Код показывает этот токен. Телеграм сверяет его в своей базе и говорит:
    «А, всё верно, ты — бот @MAtelegramAcademy_bot, проходи!».
2. *default=DefaultBotProperties(...) — это базовые правила поведения. default - по умолчанию. 
    Здесь устанавливаетcя общее правило для всех будущих сообщений бота. 
    Я говорю ему: «Что бы ты ни отправлял пользователю, всегда веди себя вот так».
   * parse_mode=ParseMode.HTML — переключатель «красивого текста»
    parse_mode - режим распознавания текста. Был выбран режим HTML.
      -Как бот видит текст без этой настройки: 
    Если вы напишете в коде "<b>Ваша анкета:</b>", бот отправит это глупо и буквально. 
    Пользователь прямо так и увидит эти скобочки в Телеграме:
    <b>Ваша анкета:</b>.
      -Как бот работает с этой настройкой: Режим HTML заставляет бота перед отправкой включить логику.
    Он видит теги <b> и </b>, стирает их, а текст между ними делает жирным
    """
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Диспетчер получает события от Telegram и передает их подходящим хендлерам.
    """
   handler - обработчик т.е. это специальная функция в коде, которая «ловит» действия 
   пользователя и решает, что делать дальше. Это ухо бота, которым он слушает Telegram. 
   Как только пользователь что-то делает, срабатывает нужный хэндлер.
   """
    dispatcher = Dispatcher()

    # Подключаем все router-объекты
    # *get_routers() = start.router, form.router
    # * распаковывает картеж роутеров из __init__.py списком через запятую, не надо каждый отдельно прописывать
    dispatcher.include_routers(*get_routers())

    # запускаем ong-pooling
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
