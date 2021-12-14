from aiogram import types

from conf import bot, settings, session


async def on_startup(dp):
    await bot.send_message(settings.admin_id, '<b>I\'m ready</b>')
    await bot.set_my_commands([
        types.BotCommand(command='help', description='Помощь 🆘'),
    ])


async def on_shutdown(dp):
    await bot.send_message(settings.admin_id, '<b>I will be back</b>')
    await session.close()


def main():
    from aiogram import executor
    import sentry_sdk

    from handlers import dp
    from middlewares.stat import StatMiddleware

    sentry_sdk.init(settings.sentry_init, traces_sample_rate=1.0)

    dp.middleware.setup(StatMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
