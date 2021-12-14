import os

import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from django.conf import settings
from telegram import Bot
import requests

try:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    django.setup()
except RuntimeError:
    pass

from .models import Question


redis_broker = RedisBroker(host='redis')
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def set_file_id(question_id: int) -> None:
    question = Question.objects.get(pk=question_id)

    if question.image_origin:
        bot = Bot(settings.TELEGRAM_API_TOKEN)
        message = bot.send_photo(settings.TELEGRAM_SUPERUSER_ID, question.image_origin)
        question.file_id = message['photo'][-1]['file_id']
        question.save()


@dramatiq.actor
def save_image_by_url(question_id: int) -> None:
    question = Question.objects.get(pk=question_id)

    if question.image_origin:
        response = requests.get(question.image_origin)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        question.image.save(f'{question.pk}.jpg', File(img_temp), save=True)


@dramatiq.actor
def send_message(user_id: int, message: str) -> None:
    Bot(settings.TELEGRAM_API_TOKEN).send_message(user_id, message)
