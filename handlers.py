import datetime

from keyboards import main_keyboard


def cmd_hello(vk, user_id, text):
    vk.messages.send(
        user_id=user_id,
        message="Привет! Я бот на vk_api. Нажми кнопку или напиши 'помощь'.",
        random_id=0,
        keyboard=main_keyboard(),
    )


def cmd_help(vk, user_id, text):
    help_text = (
        "Доступные команды:\n"
        "привет — приветствие и клавиатура\n"
        "помощь — этот список\n"
        "время — текущее время сервера\n"
        "эхо <текст> — бот повторит текст"
    )
    vk.messages.send(user_id=user_id, message=help_text, random_id=0)


def cmd_time(vk, user_id, text):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vk.messages.send(user_id=user_id, message=f"Текущее время сервера: {now}", random_id=0)


def cmd_echo(vk, user_id, text):
    payload = text[len("эхо"):].strip()
    reply = payload if payload else "Нечего повторять — напиши текст после 'эхо'."
    vk.messages.send(user_id=user_id, message=reply, random_id=0)


def cmd_unknown(vk, user_id, text):
    vk.messages.send(
        user_id=user_id,
        message="Не понимаю команду. Напиши 'помощь', чтобы увидеть список команд.",
        random_id=0,
    )


COMMANDS = {
    "привет": cmd_hello,
    "помощь": cmd_help,
    "время": cmd_time,
}


def handle_message(vk, user_id, text):
    normalized = text.strip().lower()

    if normalized.startswith("эхо"):
        cmd_echo(vk, user_id, text)
        return

    handler = COMMANDS.get(normalized, cmd_unknown)
    handler(vk, user_id, text)
