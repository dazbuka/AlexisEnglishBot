import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Тестовый токен бота
TOKEN = ''
# Боевой токен
#TOKEN = ''

#Admin's telegram ID
DEVELOPER_ID=1
TEACHER_ID=2
ADMIN_IDS=[1, 2]

DB_URL='sqlite+aiosqlite:///data/db.sqlite3'

media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/media')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, filename="log.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




