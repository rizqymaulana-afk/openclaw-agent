# telegram_sender.py

from telegram import Bot
from telegram import InputFile

import asyncio


# =========================
# TELEGRAM CONFIG
# =========================

BOT_TOKEN = "8684157124:AAGHkV4OXdUx3PHRqyVU4VBnbXWySaNnx_k"

CHAT_ID = "1003250359"


# =========================
# SEND MESSAGE
# =========================

async def send_telegram_message(
    message
):

    bot = Bot(
        token=BOT_TOKEN
    )

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )


def send_message(
    message
):

    asyncio.run(
        send_telegram_message(
            message
        )
    )


# =========================
# SEND PHOTO
# =========================

async def send_telegram_photo(
    photo_path,
    caption=None
):

    bot = Bot(
        token=BOT_TOKEN
    )

    with open(
        photo_path,
        "rb"
    ) as photo:

        await bot.send_photo(
            chat_id=CHAT_ID,
            photo=InputFile(photo),
            caption=caption
        )


def send_photo(
    photo_path,
    caption=None
):

    asyncio.run(
        send_telegram_photo(
            photo_path,
            caption
        )
    )