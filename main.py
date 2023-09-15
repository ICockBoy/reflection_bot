import logging
import asyncio
from aiogram import Bot, Dispatcher
from Routers import routers
from aiogram.fsm.storage.memory import MemoryStorage
from cred import TOKEN


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(*routers)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
