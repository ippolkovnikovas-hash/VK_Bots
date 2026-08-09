# handlers/stat_handlers.py
from config import ERROR_MESSAGES, PRIORITY_NAMES
from models import Task  # <-- ДОБАВИТЬ ЭТУ СТРОКУ
from utils.helpers import (
    calculate_productivity_score, get_weekday_stats,
    get_priority_stats, calculate_avg_completion_time,
    get_productivity_level
)


def handle_detailed_stats(send, user_id, get_user_func):
    """Подробная статистика с графиками в текстовом виде."""
    user = get_user_func(user_id)
    if not user:
        send(user_id, ERROR_MESSAGES['error_occurred'])
        return

    # Получаем статистику
    priority_stats = get_priority_stats(user)
    weekdays = get_weekday_stats(user)
    avg_completion_time = calculate_avg_completion_time(user)
    productivity = calculate_productivity_score(user)

    # Общая статистика
    total_tasks = user.tasks.count()
    completed = user.tasks.where(Task.is_done == True)  # <-- Теперь Task определен
    completed_count = completed.count()
    pending_count = total_tasks - completed_count

    import datetime
    overdue_count = user.tasks.where(
        Task.due_date < datetime.date.today(),
        Task.is_done == False
    ).count()
    today_count = user.tasks.where(Task.due_date == datetime.date.today()).count()

    level = get_productivity_level(productivity)

    stats = f"""
📈 ПРОДВИНУТАЯ СТАТИСТИКА

📊 ОБЩАЯ ИНФОРМАЦИЯ:
• Всего задач: {total_tasks}
• Выполнено: {completed_count} ({round(completed_count / total_tasks * 100, 1) if total_tasks > 0 else 0}%)
• Ожидает: {pending_count}
• Просрочено: {overdue_count}
• На сегодня: {today_count}

🎯 ПО ПРИОРИТЕТАМ (невыполненные):
{PRIORITY_NAMES[1]}: {priority_stats.get(1, 0)}
{PRIORITY_NAMES[2]}: {priority_stats.get(2, 0)}
{PRIORITY_NAMES[3]}: {priority_stats.get(3, 0)}

📅 ПО ДНЯМ НЕДЕЛИ (все задачи):
{chr(10).join([f'  {day}: {count}' for day, count in weekdays.most_common()]) if weekdays else '  Нет данных'}

⏱️ СРЕДНЕЕ ВРЕМЯ ВЫПОЛНЕНИЯ: {avg_completion_time:.1f} дней

📊 ПРОДУКТИВНОСТЬ: {productivity}%
{level}
    """
    send(user_id, stats)