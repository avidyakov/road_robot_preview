from aiogram import types
from furl import furl

from conf import settings


find_question = types.InlineKeyboardMarkup(inline_keyboard=[
    [
        types.InlineKeyboardButton(text='🔎 Найти вопрос ПДД', switch_inline_query_current_chat='')
    ],
])


def _get_buy_url(user_id: int) -> str:
    url = furl('https://oplata.qiwi.com/create')
    url.args.update({
        'publicKey': settings.qiwi_public_key,
        'billId': user_id,
        'amount': settings.amount,
        'successUrl': settings.bot_url
    })
    return url.url


def get_buy_button(user_id: int) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text='🧨 Купить полный доступ', url=_get_buy_url(user_id))
        ],
    ])
