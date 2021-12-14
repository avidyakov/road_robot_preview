import typing

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from conf import settings, session


class StatMiddleware(BaseMiddleware):

    @staticmethod
    def _get_request_data(
            user_id,
            event_type,
            first_name,
            last_name,
            username,
            locale,
            event_properties: typing.Optional[dict] = None
    ):
        if event_properties is None:
            event_properties = {}

        return {
            'api_key': settings.amplitude_key,
            'events': [
                {
                    'user_id': user_id,
                    'event_properties': {
                        'product': settings.product_name,
                        **event_properties
                    },
                    'event_type': event_type,
                    'user_propertixes': {
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username,
                        'locale': locale,
                    }
                }
            ]
        }

    async def save_event(self, data: dict) -> None:
        await session.post(settings.amplitude_url, json=data)

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        if command := data.get('command'):
            request_data = self._get_request_data(
                user_id=message.from_user.id,
                event_type=f'command_{command.command}',
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                username=message.from_user.username,
                locale=message.from_user.language_code
            )
            await self.save_event(request_data)

    async def on_post_process_inline_query(self, inline_query: types.InlineQuery, results, data: dict):
        request_data = self._get_request_data(
            user_id=inline_query.from_user.id,
            event_type=f'search_question',
            first_name=inline_query.from_user.first_name,
            last_name=inline_query.from_user.last_name,
            username=inline_query.from_user.username,
            locale=inline_query.from_user.language_code,
            event_properties={
                'query': inline_query.query,
                'offset': inline_query.offset,
                'chat_type': inline_query.chat_type,
                'inline_query_id': inline_query.id
            }
        )
        await self.save_event(request_data)

    async def on_post_process_chosen_inline_result(self, chosen_inline_result, results, data: dict):
        request_data = self._get_request_data(
            user_id=chosen_inline_result.from_user.id,
            event_type=f'chosen_inline_result',
            first_name=chosen_inline_result.from_user.first_name,
            last_name=chosen_inline_result.from_user.last_name,
            username=chosen_inline_result.from_user.username,
            locale=chosen_inline_result.from_user.language_code,
            event_properties={
                'query': chosen_inline_result.query,
                'inline_query_id': chosen_inline_result.result_id
            }
        )
        await self.save_event(request_data)
