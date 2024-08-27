from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

token = ""
bot = Bot(token)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

li = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='norm')
but2 = InlineKeyboardButton(text="Формула расчета", callback_data='form')
li.add(but1)
li.add(but2)


@dp.message_handler(commands='start')
async def start(message):
    k = [[KeyboardButton(text='Информация'), KeyboardButton(text='Рассчитать')]]
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=k)
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)



@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Информация о боте')


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    make_choice = [
        [InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='norm'),
         InlineKeyboardButton(text="Формула расчета", callback_data='form')]
    ]
    keyboard_make_choice = InlineKeyboardMarkup(inline_keyboard=make_choice)
    await message.answer('Выберите опцию:', reply_markup=keyboard_make_choice)

@dp.callback_query_handler(text='form')
async def formm(callback_query):

    tex = [
        [types.InlineKeyboardButton(text="Формула", url='https://www.calc.ru/Formula-Mifflinasan-Zheora.html')],
    ]
    keyboard_tex = types.InlineKeyboardMarkup(inline_keyboard=tex)
    await callback_query.message.answer(
        f'Формула расчета нормы калорий:\n',
        reply_markup=keyboard_tex)
    await callback_query.answer()

    # await callback_query.message.answer(
    #     'Формула расчета нормы калорий:\n'
    #     'Норма калорий = 10 * вес (кг) + 6.25 * рост (см) - 5 * возраст (лет) + 5'
    # )
    # await callback_query.answer()


@dp.callback_query_handler(text='norm')
async def nor(callback_query):
    await callback_query.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await callback_query.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(
        f"Ваша норма калорий {10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
