__version__ = "0.2.0"

import time
import logging

from driver.core import me_bot

logging.basicConfig(
  filename=f'streambot-logs-RUPU.txt',
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.getLogger("yt_dlp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("PyTgCalls").setLevel(logging.ERROR)

LOGS = logging.getLogger(__name__)
