import os

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from model import classify_image
from tokens import TG_TOKEN

bot: Bot = Bot(TG_TOKEN)
dp: Dispatcher = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Вас приветствует бот FakeFaceChecker, занимающийся отличием реальных лиц от поддельных')


@dp.message_handler(commands=['help'])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Отправьте фотографию и получите в ответ, реальное лицо или поддельное')


@dp.message_handler(content_types=['photo'])
async def ai_photo(message: types.Message):
    path: str = f'Downloads_tg/{message.photo[-1].file_id}'
    await message.photo[-1].download(path)
    await message.reply(classify_image(path))
    os.remove(path)


if __name__ == '__main__':
    executor.start_polling(dp)
