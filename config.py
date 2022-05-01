from os import getenv
from dotenv import load_dotenv

admins = {}
load_dotenv()

# client vars
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
SESSION_NAME = getenv("SESSION_NAME", "session")

# mandatory vars
OWNER_USERNAME = getenv("OWNER_USERNAME")
ALIVE_NAME = getenv("ALIVE_NAME")
BOT_USERNAME = getenv("BOT_USERNAME")
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/levina-lab/video-stream")
UPSTREAM_BRANCH = getenv("UPSTREM_BRANCH", "main")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "240"))
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "SquadGoalsss")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "shivamdemon")

# database, decorators, handlers mandatory vars
MONGODB_URL = getenv("MONGODB_URL")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! . $").split())
OWNER_ID = list(map(int, getenv("OWNER_ID").split()))
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))

# image resources vars
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/8fed8706f18cb6b378712.png")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/563c5ecd82565b21a2de3.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/7ad283944aea952d07bd5.png")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/4b7d2c8662a71abe38dcf.png")
IMG_5 = getenv("IMG_5", "https://telegra.ph/file/91a4123e0cd5d007ba1a8.png")
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/eae4f262f14b64095154f.png")
START_PIC = getenv("START_PIC", "https://telegra.ph/file/c0a31e87d7fbe60cd3c2b.png")
