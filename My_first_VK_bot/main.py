# main.py
import datetime
import logging
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from peewee import DoesNotExist

from config import BOT_TOKEN, LOG_LEVEL, ERROR_MESSAGES, HELP_MESSAGE
from models import User, create_models
from states import (
    get_state, set_state, get_data, clear_state,
    STATE_NEW_TASK_TITLE, STATE_NEW_TASK_DESCRIPTION,
    STATE_NEW_TASK_DATE, STATE_NEW_TASK_TIME,
    STATE_NEW_TASK_PRIORITY, STATE_NEW_TASK_CATEGORY,
    STATE_DELETE_TASK, STATE_TASKS_MAKE_DONE,
    STATE_ADD_CATEGORY
)
from handlers import (
    handle_start, handle_new_task, handle_tasks, handle_today,
    handle_week, handle_overdue, handle_completed, handle_delete_task,
    handle_detailed_stats, handle_add_category,
    process_task_title, process_task_description, process_task_date,
    process_task_time, process_task_priority, process_task_category,
    process_delete_task, process_task_action, process_task_done_confirmation,
    process_add_category
)
from scheduler import ReminderScheduler  # <-- ДОБАВИТЬ ИМПОРТ

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация VK
try:
    logger.info("Подключение к VK API...")
    vk_session = vk_api.VkApi(token=BOT_TOKEN)
    vk = vk_session.get_api()

    logger.info("Проверка токена...")
    groups = vk.groups.getById()
    logger.info(f"✅ Токен работает! Группа: {groups[0]['name']}")

    longpoll = VkLongPoll(vk_session)
    logger.info("✅ LongPoll создан!")

except Exception as e:
    logger.error(f"❌ Ошибка инициализации VK: {e}")
    raise

# Создание таблиц в БД
try:
    create_models()
    logger.info("✅ База данных создана/проверена!")
except Exception as e:
    logger.error(f"❌ Ошибка БД: {e}")
    raise

# Запуск планировщика напоминаний
reminder_scheduler = ReminderScheduler(vk_session)
reminder_scheduler.start()


def send(user_id, message):
    """Отправляет сообщение пользователю."""
    if not message:
        return

    try:
        if len(message) > 4000:
            parts = []
            current_part = ""
            for line in message.split('\n'):
                if len(current_part) + len(line) + 1 > 4000:
                    parts.append(current_part)
                    current_part = line
                else:
                    current_part += line + '\n'
            if current_part:
                parts.append(current_part)

            for part in parts:
                vk.messages.send(user_id=user_id, message=part, random_id=0)
        else:
            vk.messages.send(user_id=user_id, message=message, random_id=0)
    except Exception as e:
        logger.error(f"❌ Ошибка отправки сообщения: {e}")


def get_user(user_id):
    """Получает пользователя из БД или создает нового."""
    try:
        user = User.get(User.user_id == user_id)
        user.last_active = datetime.datetime.now()
        user.save()
        return user
    except DoesNotExist:
        try:
            user_info = vk.users.get(user_ids=user_id)[0]
            user = User.create(
                user_id=user_id,
                first_name=user_info["first_name"],
                last_name=user_info.get("last_name", "")
            )
            logger.info(f"✅ Создан пользователь: {user.first_name} (ID: {user_id})")
            return user
        except Exception as e:
            logger.error(f"❌ Ошибка создания пользователя: {e}")
            return None


def handle_help(user_id):
    """Помощь."""
    send(user_id, HELP_MESSAGE)


def main():
    logger.info("🚀 Бот запущен! Ожидание сообщений...")

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                try:
                    user_id = event.peer_id

                    text = event.text.strip() if hasattr(event, 'text') and event.text else ""

                    if not text:
                        continue

                    logger.info(f"📩 Сообщение от {user_id}: {text[:50]}..." if len(
                        text) > 50 else f"📩 Сообщение от {user_id}: {text}")

                    text_lower = text.lower()
                    state = get_state(user_id)

                    # Обработка команд
                    if text_lower in ["start", "/start"]:
                        handle_start(send, user_id)

                    elif text_lower in ["newtask", "/newtask"]:
                        handle_new_task(send, user_id, get_user)

                    elif text_lower in ["tasks", "/tasks"]:
                        handle_tasks(send, user_id, get_user)

                    elif text_lower in ["today", "/today"]:
                        handle_today(send, user_id, get_user)

                    elif text_lower in ["week", "/week"]:
                        handle_week(send, user_id, get_user)

                    elif text_lower in ["overdue", "/overdue"]:
                        handle_overdue(send, user_id, get_user)

                    elif text_lower in ["completed", "/completed"]:
                        handle_completed(send, user_id, get_user)

                    elif text_lower in ["stats", "/stats", "статистика"]:
                        handle_detailed_stats(send, user_id, get_user)

                    elif text_lower in ["delete", "/delete"]:
                        handle_delete_task(send, user_id, get_user)

                    elif text_lower in ["category", "/category"]:
                        handle_add_category(send, user_id)

                    elif text_lower in ["help", "/help", "помощь"]:
                        handle_help(user_id)

                    # Обработка состояний
                    elif state == STATE_NEW_TASK_TITLE:
                        process_task_title(send, user_id, text)

                    elif state == STATE_NEW_TASK_DESCRIPTION:
                        process_task_description(send, user_id, text)

                    elif state == STATE_NEW_TASK_DATE:
                        process_task_date(send, user_id, text, get_user)

                    elif state == STATE_NEW_TASK_TIME:
                        process_task_time(send, user_id, text)

                    elif state == STATE_NEW_TASK_PRIORITY:
                        process_task_priority(send, user_id, text, get_user)

                    elif state == STATE_NEW_TASK_CATEGORY:
                        process_task_category(send, user_id, text, get_user)

                    elif state == STATE_DELETE_TASK:
                        process_delete_task(send, user_id, text)

                    elif state == STATE_TASKS_MAKE_DONE:
                        data = get_data(user_id)
                        if data.get("waiting_confirmation"):
                            process_task_done_confirmation(send, user_id, text)
                        else:
                            process_task_action(send, user_id, text)

                    elif state == STATE_ADD_CATEGORY:
                        process_add_category(send, user_id, text, get_user)

                    else:
                        if text:
                            send(user_id, """
❌ Неизвестная команда.

Доступные команды:
• start - начать работу
• newtask - создать новую задачу
• tasks - последние 10 задач
• today - задачи на сегодня
• week - задачи на неделю
• overdue - просроченные задачи
• completed - выполненные задачи
• delete - удалить задачу
• stats - подробная статистика
• category - создать категорию
• help - помощь

Для изменения статуса задачи в списке введите её номер.
""")

                except Exception as e:
                    logger.error(f"❌ Ошибка обработки команды: {e}", exc_info=True)
                    try:
                        send(user_id, ERROR_MESSAGES['error_occurred'])
                        clear_state(user_id)
                    except:
                        pass

    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен.")
        reminder_scheduler.stop()
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
        reminder_scheduler.stop()


if __name__ == "__main__":
    main()