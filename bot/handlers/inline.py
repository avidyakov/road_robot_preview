import typing
from http import HTTPStatus

from aiogram import types
from furl import furl
from pydantic import BaseModel

from conf import dp, settings, messages, bot, session
from buttons.inline import find_question, get_buy_button


class Question(BaseModel):
    id: int
    question: str
    answer: str
    hint: str
    image_url: typing.Optional[str]


class QuestionsResponse(BaseModel):
    count: int
    next: typing.Optional[str]
    previous: typing.Optional[str]
    results: list[Question]


class User(BaseModel):
    chosen_query_count: int
    access: bool


@dp.inline_handler()
async def query_questions(inline_query: types.InlineQuery):
    user_url: str = (furl(settings.api_url) / f'telegram/users/{inline_query.from_user.id}/').url
    async with session.get(user_url) as response:
        if response.status == HTTPStatus.NOT_FOUND.value:
            kwargs = {
                'results': [],
                'is_personal': True,
                'cache_time': 0,
                'switch_pm_text': 'Нажмите, чтобы продолжить',
                'switch_pm_parameter': 'test'
            }
            await inline_query.answer(**kwargs)
            return

        user = User(**await response.json())

    questions_url = furl(settings.api_url) / 'questions/'
    questions_url.args['search'] = inline_query.query
    questions_url.args['offset'] = inline_query.offset or 0

    async with session.get(questions_url.url) as response:
        questions = QuestionsResponse(**await response.json())

    results = []
    buy_button = get_buy_button(inline_query.from_user.id)
    for question in questions.results:
        image_url = furl(settings.api_url) / question.image_url if question.image_url else ''
        image_url = image_url.url if image_url else ''

        caption = messages['answer_template'].format(
            question=question.question,
            answer=question.answer,
            hint=question.hint,
            image=image_url
        )[:1024] if user.access else messages['purchase_offer']

        inline_query_result = types.InlineQueryResultArticle(
            id=question.id,
            title=question.question,
            thumb_url=image_url,
            input_message_content=types.InputTextMessageContent(caption),
            reply_markup=find_question if user.access else buy_button,
        )

        results.append(inline_query_result)

    args = {
        'results': results,
        'is_personal': True,
        'cache_time': 0
    }

    if questions.next:
        args['next_offset'] = furl(questions.next).args['offset']

    await inline_query.answer(**args)


@dp.chosen_inline_handler()
async def update_chosen_inline_query_count(chosen_inline_query: types.ChosenInlineResult):
    user_url = (furl(settings.api_url) / f'telegram/users/{chosen_inline_query.from_user.id}/').url

    async with session.get(user_url) as response:
        user = User(**await response.json())

    user.chosen_query_count += 1
    await session.patch(user_url, json=user.dict())
