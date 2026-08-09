# utils/helpers.py
import datetime
import logging
from collections import Counter
from models import Task

logger = logging.getLogger(__name__)


def calculate_productivity_score(user):
    """Расчет продуктивности пользователя."""
    if not user:
        return 0

    total = user.tasks.count()
    if total == 0:
        return 0

    completed = user.tasks.where(Task.is_done == True).count()
    base_score = (completed / total) * 100

    # Бонус за выполнение в срок
    on_time = user.tasks.where(
        Task.is_done == True,
        Task.completed_at <= Task.due_date
    ).count()
    bonus = (on_time / total) * 20 if total > 0 else 0

    return min(100, base_score + bonus)


def get_weekday_stats(user):
    """Получить статистику по дням недели."""
    weekdays = Counter()
    tasks = user.tasks.where(Task.is_done == False)
    for task in tasks:
        if task.due_date:
            weekdays[task.due_date.strftime('%A')] += 1
    return weekdays


def get_priority_stats(user):
    """Получить статистику по приоритетам."""
    priority_stats = {}
    for priority in [1, 2, 3]:
        count = user.tasks.where(Task.priority == priority, Task.is_done == False).count()
        priority_stats[priority] = count
    return priority_stats


def calculate_avg_completion_time(user):
    """Рассчитать среднее время выполнения задачи."""
    completed = user.tasks.where(Task.is_done == True)
    avg_completion_time = 0

    if completed.count() > 0:
        total_days = 0
        valid_tasks = 0
        for task in completed:
            if task.completed_at and task.created_at:
                days_diff = (task.completed_at.date() - task.created_at.date()).days
                if days_diff >= 0:
                    total_days += days_diff
                    valid_tasks += 1

        if valid_tasks > 0:
            avg_completion_time = total_days / valid_tasks

    return avg_completion_time


def format_task_list(tasks, title="📋 Список задач"):
    """Форматировать список задач для отправки."""
    if not tasks:
        return "📭 Нет задач."

    result = [f"{title}:\n"]
    for task in tasks:
        result.append(str(task))

    return "\n".join(result)


def get_productivity_level(score):
    """Определить уровень продуктивности."""
    if score >= 80:
        return "⭐ Отлично!"
    elif score >= 60:
        return "💪 Хорошо!"
    elif score >= 40:
        return "📈 Есть куда расти!"
    else:
        return "🎯 Нужно больше работать!"