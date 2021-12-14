from aiogram import types
from aiogram.dispatcher.filters import IsReplyFilter
from furl import furl

from conf import dp, settings, messages, session
from buttons.inline import find_question


@dp.message_handler(commands=['start'])
async def start_command(msg: types.Message):
    await msg.answer('👋')
    await types.ChatActions.typing(2)

    request_data = {
        'id': msg.from_user.id,
        'username': msg.from_user.username,
        'first_name': msg.from_user.first_name,
        'last_name': msg.from_user.last_name
    }
    user_url = furl(settings.api_url) / 'telegram/users/'
    await session.post(user_url.url, json=request_data)

    await msg.answer_animation(settings.video_file_id)
    await types.ChatActions.typing(1)
    await msg.answer(messages['help'], reply_markup=find_question)


@dp.message_handler(commands=['help'])
async def help_command(msg: types.Message):
    await types.ChatActions.typing(2)
    await msg.answer_animation(settings.video_file_id)
    await types.ChatActions.typing(1)
    await msg.answer(messages['help'], reply_markup=find_question)


@dp.message_handler(IsReplyFilter(True), commands=['file_id'])
async def get_file_id(msg: types.Message):
    if msg.reply_to_message.animation:
        await msg.answer(msg.reply_to_message.animation.file_id)
