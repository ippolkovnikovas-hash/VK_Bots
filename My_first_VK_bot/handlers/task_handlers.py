# handlers/task_handlers.py
import datetime
import logging
from config import (
    DATE_FORMAT, ERROR_MESSAGES, SUCCESS_MESSAGES,
    PRIORITY_NAMES, MAX_TASKS_PER_USER, TASKS_PER_PAGE
)
from models import User, Task, TaskCategory, Reminder
from states import (
    get_state, set_state, get_data, clear_state,
    STATE_NEW_TASK_TITLE, STATE_NEW_TASK_DESCRIPTION,
    STATE_NEW_TASK_DATE, STATE_NEW_TASK_TIME,
    STATE_NEW_TASK_PRIORITY, STATE_NEW_TASK_CATEGORY,
    STATE_DELETE_TASK, STATE_TASKS_MAKE_DONE
)

logger = logging.getLogger(__name__)


def get_user(user_id):
    """Получает пользователя из БД или создает нового."""
    try:
        user = User.get(User.user_id == user_id)
        user.last_active = datetime.datetime.now()
        user.save()
        return user
    except User.DoesNotExist:
        return None


def handle_start(send, user_id):
    """Обработка команды start."""
    from config import WELCOME_MESSAGE
    user = get_user(user_id)  # Используйте переданную функцию
    if user:
        send(user_id, WELCOME_MESSAGE)
        clear_state(user_id)


def handle_new_task(send, user_id, get_user_func):
    """Начало процесса создания задачи."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    if user.tasks.count() >= MAX_TASKS_PER_USER:
        send(user_id, ERROR_MESSAGES['task_limit_reached'])
        return

    send(user_id, "📝 Введите название задачи:")
    set_state(user_id, STATE_NEW_TASK_TITLE, {"user_id": user_id})


def process_task_title(send, user_id, text):
    """Обработка названия задачи."""
    if not text or len(text.strip()) == 0:
        send(user_id, ERROR_MESSAGES['empty_title'])
        return

    data = get_data(user_id)
    data["title"] = text.strip()
    set_state(user_id, STATE_NEW_TASK_DESCRIPTION, data)
    send(user_id, "📄 Введите описание задачи (или '-' чтобы пропустить):")


def process_task_description(send, user_id, text):
    """Обработка описания задачи."""
    data = get_data(user_id)
    if text and text != "-":
        data["description"] = text.strip()
    set_state(user_id, STATE_NEW_TASK_DATE, data)
    send(user_id, f"📅 Введите дату выполнения (ДД.ММ.ГГГГ):")


def process_task_date(send, user_id, text, get_user_func):
    """Обработка даты задачи."""
    try:
        due_date = datetime.datetime.strptime(text.strip(), DATE_FORMAT).date()
        if due_date < datetime.date.today():
            send(user_id, "⚠️ Дата не может быть в прошлом. Введите корректную дату (ДД.ММ.ГГГГ):")
            return
    except ValueError:
        send(user_id, ERROR_MESSAGES['invalid_date'])
        return

    data = get_data(user_id)
    data["due_date"] = due_date
    set_state(user_id, STATE_NEW_TASK_TIME, data)
    send(user_id, "⏰ Введите время выполнения (ЧЧ:ММ) или '-' чтобы пропустить:")


def process_task_time(send, user_id, text):
    """Обработка времени задачи."""
    data = get_data(user_id)
    if text and text != "-":
        try:
            due_time = datetime.datetime.strptime(text.strip(), "%H:%M").time()
            data["due_time"] = due_time
        except ValueError:
            send(user_id, ERROR_MESSAGES['invalid_time'])
            return

    set_state(user_id, STATE_NEW_TASK_PRIORITY, data)
    send(user_id, f"""
🔰 Выберите приоритет задачи:
1 - {PRIORITY_NAMES[1]}
2 - {PRIORITY_NAMES[2]}
3 - {PRIORITY_NAMES[3]}

Введите номер приоритета (1, 2 или 3):
""")


def process_task_priority(send, user_id, text, get_user_func):
    """Обработка приоритета задачи."""
    try:
        priority = int(text.strip())
        if priority not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        send(user_id, "❌ Введите число 1, 2 или 3:")
        return

    data = get_data(user_id)
    data["priority"] = priority

    user = get_user_func(user_id)
    categories = list(user.categories)

    if categories:
        set_state(user_id, STATE_NEW_TASK_CATEGORY, data)
        response = "📂 Выберите категорию для задачи:\n"
        for i, cat in enumerate(categories, 1):
            response += f"{i}. {cat.name}\n"
        response += "0. Без категории\n\nВведите номер категории:"
        send(user_id, response)
    else:
        save_task(send, user_id, data)


def process_task_category(send, user_id, text, get_user_func):
    """Обработка категории задачи."""
    try:
        choice = int(text.strip())
        data = get_data(user_id)

        if choice != 0:
            user = get_user_func(user_id)
            categories = list(user.categories)
            if 1 <= choice <= len(categories):
                data["category"] = categories[choice - 1]
            else:
                send(user_id, "❌ Неверный номер категории. Введите номер из списка:")
                return

        save_task(send, user_id, data)
    except ValueError:
        send(user_id, "❌ Введите номер категории:")
        return


def save_task(send, user_id, data):
    """Создание и сохранение задачи."""
    try:
        user = get_user(user_id)
        task_data = {
            "user": user,
            "title": data["title"],
            "description": data.get("description"),
            "due_date": data["due_date"],
            "due_time": data.get("due_time"),
            "priority": data.get("priority", 2)
        }

        task = Task.create(**task_data)

        if "category" in data:
            TaskCategory.create(task=task, category=data["category"])

        clear_state(user_id)
        send(user_id, f"{SUCCESS_MESSAGES['task_created']}\n{task.get_full_info()}")

        # ========== ИСПРАВЛЕННАЯ ЧАСТЬ ==========
        # Создаем напоминание для задачи
        import datetime

        today = datetime.date.today()

        # Если задача на сегодня или в будущем
        if task.due_date >= today:
            reminder_time = None

            if task.due_date == today:
                # Если задача на сегодня - напоминание в указанное время
                if task.due_time:
                    reminder_time = datetime.datetime.combine(today, task.due_time)
                else:
                    # Если время не указано - через 1 час от текущего момента
                    reminder_time = datetime.datetime.now() + datetime.timedelta(hours=1)

                # Если время уже прошло - напоминание через 5 минут
                if reminder_time < datetime.datetime.now():
                    reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=5)

            else:
                # Если задача в будущем - напоминание за день до дедлайна в 9:00
                reminder_time = datetime.datetime.combine(
                    task.due_date - datetime.timedelta(days=1),
                    datetime.time(9, 0)
                )

            # Создаем напоминание
            if reminder_time:
                Reminder.create(
                    task=task,
                    reminder_time=reminder_time,
                    is_sent=False
                )
                send(user_id, f"⏰ Напоминание установлено на {reminder_time.strftime('%d.%m.%Y %H:%M')}")

        # ======================================

    except Exception as e:
        logger.error(f"Error saving task: {e}")
        clear_state(user_id)
        send(user_id, ERROR_MESSAGES['error_occurred'])


def handle_tasks(send, user_id, get_user_func):
    """Показать последние задачи."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    tasks = user.tasks.order_by(-Task.due_date, -Task.task_id).limit(TASKS_PER_PAGE)

    if not tasks:
        send(user_id, ERROR_MESSAGES['no_tasks'])
        return

    result = [f"📋 Последние {TASKS_PER_PAGE} задач:\n"]
    for task in tasks:
        result.append(str(task))

    result.append("\n💡 Введите номер задачи, чтобы изменить её статус или получить подробную информацию.")
    send(user_id, "\n".join(result))
    set_state(user_id, STATE_TASKS_MAKE_DONE)


def handle_today(send, user_id, get_user_func):
    """Показать задачи на сегодня."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    tasks = user.tasks.where(Task.due_date == datetime.date.today())

    if not tasks:
        send(user_id, "🎉 На сегодня задач нет!")
        return

    result = ["📅 Задачи на сегодня:\n"]
    for task in tasks:
        result.append(str(task))

    result.append("\n💡 Введите номер задачи, чтобы изменить её статус.")
    send(user_id, "\n".join(result))
    set_state(user_id, STATE_TASKS_MAKE_DONE)


def handle_week(send, user_id, get_user_func):
    """Показать задачи на неделю."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    today = datetime.date.today()
    week_end = today + datetime.timedelta(days=7)

    tasks = user.tasks.where(
        (Task.due_date >= today) &
        (Task.due_date <= week_end) &
        (Task.is_done == False)
    ).order_by(Task.due_date)

    if not tasks:
        send(user_id, "📭 Нет задач на ближайшую неделю.")
        return

    result = ["📅 Задачи на неделю:\n"]
    current_date = None
    for task in tasks:
        if task.due_date != current_date:
            current_date = task.due_date
            result.append(f"\n📌 {task.due_date.strftime(DATE_FORMAT)}:")
        result.append(f"  {task}")

    send(user_id, "\n".join(result))


def handle_overdue(send, user_id, get_user_func):
    """Показать просроченные задачи."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    today = datetime.date.today()
    tasks = user.tasks.where(
        (Task.due_date < today) &
        (Task.is_done == False)
    ).order_by(Task.due_date)

    if not tasks:
        send(user_id, "✅ Нет просроченных задач!")
        return

    result = ["⚠️ Просроченные задачи:\n"]
    for task in tasks:
        result.append(f"❗ {task}")

    send(user_id, "\n".join(result))


def handle_completed(send, user_id, get_user_func):
    """Показать выполненные задачи."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    tasks = user.tasks.where(Task.is_done == True).order_by(-Task.completed_at).limit(TASKS_PER_PAGE)

    if not tasks:
        send(user_id, "📭 Нет выполненных задач.")
        return

    result = ["✅ Выполненные задачи:\n"]
    for task in tasks:
        result.append(str(task))

    send(user_id, "\n".join(result))


def handle_delete_task(send, user_id, get_user_func):
    """Начало удаления задачи."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    tasks = user.tasks.where(Task.is_done == True).limit(TASKS_PER_PAGE)
    if not tasks:
        send(user_id, "📭 Нет выполненных задач для удаления.")
        return

    result = ["🗑️ Выберите задачу для удаления:\n"]
    for task in tasks:
        result.append(str(task))

    result.append("\nВведите номер задачи для удаления:")
    send(user_id, "\n".join(result))
    set_state(user_id, STATE_DELETE_TASK)


def process_delete_task(send, user_id, text):
    """Удаление задачи."""
    try:
        task_id = int(text.strip())
    except ValueError:
        send(user_id, ERROR_MESSAGES['invalid_number'])
        return

    task = Task.get_or_none(Task.task_id == task_id)
    if not task:
        send(user_id, ERROR_MESSAGES['task_not_found'])
        return

    if task.user_id != user_id:
        send(user_id, ERROR_MESSAGES['not_your_task'])
        return

    if not task.is_done:
        send(user_id, ERROR_MESSAGES['cannot_delete_active'])
        return

    task.delete_instance(recursive=True)
    clear_state(user_id)
    send(user_id, SUCCESS_MESSAGES['task_deleted'])


def process_task_action(send, user_id, text):
    """Обработка выбора задачи для изменения статуса."""
    try:
        task_id = int(text.strip())
    except ValueError:
        send(user_id, ERROR_MESSAGES['invalid_number'])
        return

    task = Task.get_or_none(Task.task_id == task_id)
    if not task:
        send(user_id, ERROR_MESSAGES['task_not_found'])
        return

    if task.user_id != user_id:
        send(user_id, ERROR_MESSAGES['not_your_task'])
        return

    send(user_id, task.get_full_info())
    send(user_id, "Хотите изменить статус задачи? (да/нет)")
    set_state(user_id, STATE_TASKS_MAKE_DONE, {"task_id": task_id, "waiting_confirmation": True})


def process_task_done_confirmation(send, user_id, text):
    """Подтверждение изменения статуса задачи."""
    data = get_data(user_id)
    task_id = data.get("task_id")

    if not task_id:
        clear_state(user_id)
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    task = Task.get_or_none(Task.task_id == task_id)
    if not task:
        clear_state(user_id)
        send(user_id, ERROR_MESSAGES['task_not_found'])
        return

    if text.lower() in ["да", "+", "yes", "y", "lf"]:
        if task.is_done:
            send(user_id, "Задача уже выполнена.")
        else:
            task.mark_done()
            send(user_id, f"{SUCCESS_MESSAGES['task_completed']}\n{task}")
    else:
        send(user_id, SUCCESS_MESSAGES['operation_cancelled'])

    clear_state(user_id)