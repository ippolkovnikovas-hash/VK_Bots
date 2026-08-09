# handlers/category_handlers.py
from peewee import IntegrityError
from config import ERROR_MESSAGES, SUCCESS_MESSAGES
from models import Category
from states import set_state, get_state, get_data, clear_state, STATE_ADD_CATEGORY


def handle_add_category(send, user_id):
    """Добавление новой категории."""
    send(user_id, "📂 Введите название новой категории:")
    set_state(user_id, STATE_ADD_CATEGORY)


def process_add_category(send, user_id, text, get_user_func):
    """Обработка создания категории."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        clear_state(user_id)
        return

    if not text or len(text.strip()) == 0:
        send(user_id, "❌ Название категории не может быть пустым.")
        return

    try:
        category = Category.create(user=user, name=text.strip())
        clear_state(user_id)
        send(user_id, f"{SUCCESS_MESSAGES['category_created']} '{category.name}'!")
    except IntegrityError:
        send(user_id, ERROR_MESSAGES['category_exists'])