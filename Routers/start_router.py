import asyncio
from aiogram import Router, F, Bot
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.types import FSInputFile
from messages import MESSAGES
from aiogram.utils.keyboard import InlineKeyboardBuilder
from Database import DataBase

start = Router()


@start.message(Command("btn"))
async def create_buttons(message: Message, bot: Bot):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Забронировать сессию", url="https://olga-sedakova.reservio.com/"))
    keyboard.add(InlineKeyboardButton(text="Написать в Whatsapp", url="https://wa.me/+79774916345"))
    keyboard.add(InlineKeyboardButton(text="Как проходят коуч-сессии", url="olgagrigorieva.ru"))
    keyboard.adjust(1)
    await bot.send_message(chat_id=-1002292430247, text="Меню:", reply_markup=keyboard.as_markup())


async def pendingMessage(message: Message, text: str, keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()):
    await asyncio.sleep(5)
    await message.answer(text=text, reply_markup=keyboard.as_markup())


@start.message(Command('start'))
async def startCMD(message: Message):
    db = DataBase()
    await message.delete()
    if str(message.from_user.id) not in db.data:
        db.setUsrInfo(str(message.from_user.id), 0)
        await message.answer_photo(
            photo=FSInputFile("Resources/image1.png"),
            caption=MESSAGES.aboutMsg.value)

        await asyncio.create_task(pendingMessage(message, MESSAGES.helloMsg.value))

        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text="Да", callback_data="yes"),
                     InlineKeyboardButton(text="Нет", callback_data="no"))

        await asyncio.create_task(pendingMessage(message, MESSAGES.infoMsg.value, keyboard))
    else:
        return


@start.message(Command("subscribe"))
async def subscribe(message: Message):
    await message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Записаться", url="https://olga-sedakova.reservio.com/"))
    await message.answer(text="Забронировать сессию можно здесь", reply_markup=keyboard.as_markup())


@start.message(Command("contact"))
async def subscribe(message: Message):
    await message.delete()
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Написать в Whatsapp", url="https://wa.me/+79774916345"))
    await message.answer(text="Перейти в чат", reply_markup=keyboard.as_markup())


@start.message(Command("info"))
async def subscribe(message: Message):
    await message.delete()
    await message.answer(text="О том, как проходят коуч-сессии, можно почитать на моем сайте:"
                              "\nolgagrigorieva.ru")


@start.callback_query(F.data == "no")
async def reflectionNotification(callback: CallbackQuery):
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        text="Отлично! Если Вы почувствуете, что время рефлексии пришло, то просто напишите /reflection или "
             "воспользуейтесь меню команд!")
    await callback.answer()


