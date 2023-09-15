from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from messages import NOTIFICATIONS_MESSAGES, REFLECTION_MESSAGES
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler as BackgroundScheduler
from datetime import datetime
from Routers.questions_router import QuestionsLine

notifications = Router()


class NotificationsSetup(StatesGroup):
    timeZone = State()
    notificationTime = State()


async def timeChecker(time: str) -> bool:
    if time.find(":") > 0:
        try:
            temp = list(map(int, time.split(":")))
            if temp[0] > 24 or temp[0] < 0:
                return False
            if temp[1] > 60 or temp[1] < 0:
                return False
            return True
        except:
            return False
    else:
        return False


async def startReflection(message: Message, state: FSMContext):
    await state.set_state(QuestionsLine.polling)
    await message.answer(text=list(REFLECTION_MESSAGES)[0].value)
    await state.set_data({"numOfQ": 1})


@notifications.callback_query(F.data == "yes")
async def setupNotifications(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete_reply_markup()
    await callback.message.answer(text=NOTIFICATIONS_MESSAGES.timeZoneMsg.value, parse_mode="HTML")
    await state.set_state(NotificationsSetup.timeZone)
    await callback.answer()


@notifications.message(NotificationsSetup.timeZone)
async def setupNotificationTime(message: Message, state: FSMContext):
    if await timeChecker(str(message.text)):
        await state.set_data({"usrTime": int(message.text[:2])})
        await message.answer(text=NOTIFICATIONS_MESSAGES.notificationTime.value)
        await state.set_state(NotificationsSetup.notificationTime)
    else:
        await message.answer(text="Неверный формат времени!\nповторите попытку:")


@notifications.message(NotificationsSetup.notificationTime)
async def setupNotificationTime(message: Message, state: FSMContext):
    if await timeChecker(str(message.text)):
        needTime = int(message.text[:2])
        timeZone = await state.get_data()
        timeZone = int(datetime.now().hour) - int(list(timeZone.values())[0])
        await message.answer(text=NOTIFICATIONS_MESSAGES.timeSucces.value)
        await state.clear()
        scheduler = BackgroundScheduler()
        scheduler.add_job(startReflection, 'cron', hour=needTime-timeZone, minute=int(message.text[3:]),
                          args=[message, state])
        scheduler.start()
    else:
        await message.answer(text="Неверный формат времени!\nповторите попытку:")
