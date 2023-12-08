import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import bot, dp
from telegram.common.middlewares import ChekUserReg
from telegram.handlers.main_handler import main_router

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.outer_middleware(ChekUserReg())
    dp.callback_query.outer_middleware(ChekUserReg())
    dp.include_routers(main_router)
    print('telegram\'ve started')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
