import os
from dotenv import load_dotenv

load_dotenv()

VK_GROUP_TOKEN = os.getenv("VK_GROUP_TOKEN")
VK_GROUP_ID = os.getenv("VK_GROUP_ID")

if not VK_GROUP_TOKEN or not VK_GROUP_ID:
    raise RuntimeError(
        "Не найдены VK_GROUP_TOKEN или VK_GROUP_ID. "
        "Скопируйте .env.example в .env и заполните значения."
    )
