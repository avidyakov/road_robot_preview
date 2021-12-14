from pathlib import Path

import toml
from aiogram import Bot, Dispatcher, types
import aiohttp
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    api_key: str = Field(env='API_KEY')
    admin_id: int = Field(env='ADMIN_ID')
    api_url: str = Field(env='API_URL')
    amplitude_key: str = Field(env='AMPLITUDE_KEY')
    amplitude_url: str = Field(env='AMPLITUDE_URL')
    product_name: str = 'road_robot'
    inline_query_limit: int = 3
    qiwi_public_key: str = Field(env='QIWI_PUBLIC_KEY')
    amount: int = 99
    bot_url: str = Field(env='BOT_URL')
    video_file_id: str = Field(env='VIDEO_FILE_ID')
    sentry_init: str = Field(env='SENTRY_INIT')

    class Config:
        env_file_encoding = 'utf-8'


settings = Settings()
messages = toml.loads(Path('messages.toml').read_text())
bot = Bot(settings.api_key, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
