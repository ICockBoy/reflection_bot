from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from messages import REFLECTION_MESSAGES, MESSAGES
from Database import DataBase
from cred import MSG_TESTS

questions = Router()


class QuestionsLine(StatesGroup):
    polling = State()


@questions.message(Command("reflection"))
async def startReflection(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(QuestionsLine.polling)
    await message.answer(text=list(REFLECTION_MESSAGES)[0].value)
    await state.set_data({"numOfQ": 1})


@questions.message(QuestionsLine.polling)
async def reflection(message: Message, state: FSMContext):
    numOfQ = await state.get_data()
    numOfQ = list(numOfQ.values())[0]
    if numOfQ < len(REFLECTION_MESSAGES):
        await message.answer(text=list(REFLECTION_MESSAGES)[numOfQ].value)
        numOfQ += 1
        await state.set_data({"numOfQ": numOfQ})
    else:
        db = DataBase()
        N = db.getUsrInfo(message.from_user.id) - 1
        if N <= 0:
            N = MSG_TESTS
            kb = InlineKeyboardBuilder().add(
                InlineKeyboardButton(url="https://wa.me/+79774916345", text="Перейти в WhatsApp"))
            await message.answer(text=MESSAGES.adMsg.value, reply_markup=kb.as_markup())
        db.setUsrInfo(message.from_user.id, N)
        await state.clear()
