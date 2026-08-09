# config.py
import os
from dotenv import load_dotenv

# Подгружаем переменные из файла .env (если он есть)
load_dotenv()


class Config:
    """Класс для хранения конфигурации."""

    # ========== ОСНОВНЫЕ НАСТРОЙКИ ==========

    # Путь к базе данных
    DB_PATH = os.getenv("DB_PATH", "database/database.db")

    # Токен сообщества VK
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # ========== ФОРМАТЫ ДАТ ==========

    DATE_FORMAT = "%d.%m.%Y"
    DATETIME_FORMAT = "%d.%m.%Y %H:%M"
    TIME_FORMAT = "%H:%M"

    # ========== НАСТРОЙКИ ПРИЛОЖЕНИЯ ==========

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    MAX_TASKS_PER_USER = int(os.getenv("MAX_TASKS_PER_USER", "100"))
    DEFAULT_PRIORITY = int(os.getenv("DEFAULT_PRIORITY", "2"))
    ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "true").lower() == "true"
    REMINDER_CHECK_INTERVAL = int(os.getenv("REMINDER_CHECK_INTERVAL", "3600"))
    TASKS_PER_PAGE = int(os.getenv("TASKS_PER_PAGE", "10"))

    # ========== СООБЩЕНИЯ ==========

    WELCOME_MESSAGE = """
Добро пожаловать в менеджер задач! 📋

Доступные команды:
• start - начать работу
• newtask - создать новую задачу
• tasks - показать последние 10 задач
• today - задачи на сегодня
• week - задачи на неделю
• overdue - просроченные задачи
• completed - выполненные задачи
• delete - удалить задачу
• stats - подробная статистика
• category - создать категорию
• help - помощь

Для изменения статуса задачи в списке введите её номер.
"""

    HELP_MESSAGE = """
📚 ПОМОЩЬ ПО КОМАНДАМ:

🔹 start - регистрация и приветствие
🔹 newtask - создание новой задачи (пошаговый мастер)
🔹 tasks - список последних 10 задач
🔹 today - задачи на сегодня
🔹 week - задачи на ближайшую неделю
🔹 overdue - просроченные задачи
🔹 completed - выполненные задачи
🔹 delete - удаление выполненной задачи
🔹 stats - подробная статистика и продуктивность
🔹 category - создание категории для задач
🔹 help - эта справка

📌 Чтобы изменить статус задачи, введите её номер из списка.
"""

    ERROR_MESSAGES = {
        'not_registered': "❌ Вы не зарегистрированы. Напишите: start",
        'invalid_date': "❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ",
        'invalid_time': "❌ Неверный формат времени. Используйте ЧЧ:ММ",
        'invalid_number': "❌ Введите числовой номер.",
        'task_not_found': "❌ Задачи с таким номером не существует.",
        'not_your_task': "❌ Это не ваша задача.",
        'no_tasks': "📭 У вас пока нет задач.",
        'task_limit_reached': "⚠️ Достигнут лимит задач.",
        'error_occurred': "❌ Произошла ошибка. Попробуйте позже.",
        'empty_title': "❌ Название не может быть пустым.",
        'category_exists': "❌ Категория с таким названием уже существует.",
        'cannot_delete_active': "❌ Можно удалять только выполненные задачи.",
    }

    SUCCESS_MESSAGES = {
        'task_created': "✅ Задача создана!",
        'task_deleted': "✅ Задача удалена.",
        'task_completed': "✅ Статус обновлён!",
        'category_created': "✅ Категория создана!",
        'operation_cancelled': "Операция отменена.",
    }

    PRIORITY_NAMES = {
        1: "🔴 Высокий",
        2: "🟡 Средний",
        3: "🟢 Низкий"
    }

    PRIORITY_EMOJIS = {
        1: "🔴",
        2: "🟡",
        3: "🟢"
    }

    # ========== ВАЛИДАЦИЯ ==========

    @classmethod
    def validate(cls):
        """Проверка обязательных настроек."""
        if not cls.BOT_TOKEN:
            raise RuntimeError(
                "BOT_TOKEN не задан. Создайте файл .env на основе .env.example "
                "и укажите в нём BOT_TOKEN=..."
            )

        if cls.MAX_TASKS_PER_USER < 1:
            raise ValueError("MAX_TASKS_PER_USER должен быть больше 0")

        if cls.TASKS_PER_PAGE < 1:
            raise ValueError("TASKS_PER_PAGE должен быть больше 0")

        if cls.DEFAULT_PRIORITY not in [1, 2, 3]:
            raise ValueError("DEFAULT_PRIORITY должен быть 1, 2 или 3")

        if cls.REMINDER_CHECK_INTERVAL < 60:
            raise ValueError("REMINDER_CHECK_INTERVAL должен быть не менее 60 секунд")

        return True

    @classmethod
    def get_priority_name(cls, priority):
        """Получить название приоритета."""
        return cls.PRIORITY_NAMES.get(priority, "🟡 Средний")

    @classmethod
    def get_priority_emoji(cls, priority):
        """Получить эмодзи приоритета."""
        return cls.PRIORITY_EMOJIS.get(priority, "🟡")


# Создаем экземпляр конфига
config = Config()

# Валидируем при импорте
config.validate()

# Для удобства можно экспортировать переменные напрямую
DB_PATH = config.DB_PATH
BOT_TOKEN = config.BOT_TOKEN
DATE_FORMAT = config.DATE_FORMAT
DATETIME_FORMAT = config.DATETIME_FORMAT
TIME_FORMAT = config.TIME_FORMAT
LOG_LEVEL = config.LOG_LEVEL
MAX_TASKS_PER_USER = config.MAX_TASKS_PER_USER
DEFAULT_PRIORITY = config.DEFAULT_PRIORITY
ENABLE_NOTIFICATIONS = config.ENABLE_NOTIFICATIONS
REMINDER_CHECK_INTERVAL = config.REMINDER_CHECK_INTERVAL
TASKS_PER_PAGE = config.TASKS_PER_PAGE
WELCOME_MESSAGE = config.WELCOME_MESSAGE
HELP_MESSAGE = config.HELP_MESSAGE
ERROR_MESSAGES = config.ERROR_MESSAGES
SUCCESS_MESSAGES = config.SUCCESS_MESSAGES
PRIORITY_NAMES = config.PRIORITY_NAMES
PRIORITY_EMOJIS = config.PRIORITY_EMOJIS