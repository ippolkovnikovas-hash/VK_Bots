# scheduler.py
import datetime
import logging
import threading
import time
from config import REMINDER_CHECK_INTERVAL, ENABLE_NOTIFICATIONS
from models import Reminder, Task
import vk_api

logger = logging.getLogger(__name__)


class ReminderScheduler:
    """Класс для управления напоминаниями."""

    def __init__(self, vk_session):
        self.vk = vk_session.get_api()
        self.running = False
        self.thread = None

    def start(self):
        """Запуск планировщика в отдельном потоке."""
        if not ENABLE_NOTIFICATIONS:
            logger.info("🔕 Уведомления отключены в настройках")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info(f"⏰ Планировщик напоминаний запущен (интервал: {REMINDER_CHECK_INTERVAL}с)")

    def stop(self):
        """Остановка планировщика."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("⏰ Планировщик напоминаний остановлен")

    def _run(self):
        """Основной цикл планировщика."""
        while self.running:
            try:
                self._check_reminders()
                self._check_deadlines()
                time.sleep(REMINDER_CHECK_INTERVAL)
            except Exception as e:
                logger.error(f"❌ Ошибка в планировщике: {e}")
                time.sleep(60)

    def _check_reminders(self):
        """Проверка и отправка напоминаний."""
        now = datetime.datetime.now()

        # Находим непосланные напоминания
        reminders = Reminder.select().where(
            Reminder.is_sent == False,
            Reminder.reminder_time <= now
        )

        for reminder in reminders:
            try:
                task = reminder.task
                user_id = task.user.user_id

                message = f"""
⏰ НАПОМИНАНИЕ!

📌 Задача: {task.title}
📅 Дедлайн: {task.due_date.strftime('%d.%m.%Y')}
{'⏰ Время: ' + task.due_time.strftime('%H:%M') if task.due_time else ''}
{'📝 Описание: ' + task.description if task.description else ''}

⚠️ Время выполнения задачи наступило!
"""
                # Отправляем сообщение
                self.vk.messages.send(
                    user_id=user_id,
                    message=message,
                    random_id=0
                )

                # Отмечаем напоминание как отправленное
                reminder.is_sent = True
                reminder.save()

                logger.info(f"✅ Отправлено напоминание для задачи #{task.task_id}")

            except Exception as e:
                logger.error(f"❌ Ошибка отправки напоминания: {e}")

    def _check_deadlines(self):
        """Проверка приближающихся дедлайнов."""
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)

        # Ищем задачи с дедлайном завтра
        tasks = Task.select().where(
            Task.due_date == tomorrow,
            Task.is_done == False
        )

        for task in tasks:
            try:
                # Проверяем, не отправляли ли уже напоминание
                existing = Reminder.select().where(
                    Reminder.task == task,
                    Reminder.is_sent == True,
                    Reminder.reminder_time >= datetime.datetime.now() - datetime.timedelta(days=1)
                )

                if existing.count() > 0:
                    continue

                user_id = task.user.user_id

                message = f"""
⚠️ ПРЕДУПРЕЖДЕНИЕ!

📌 Задача: {task.title}
📅 Дедлайн ЗАВТРА: {task.due_date.strftime('%d.%m.%Y')}
{'⏰ Время: ' + task.due_time.strftime('%H:%M') if task.due_time else ''}

🔥 Не забудьте выполнить задачу!
"""
                self.vk.messages.send(
                    user_id=user_id,
                    message=message,
                    random_id=0
                )

                logger.info(f"✅ Отправлено предупреждение для задачи #{task.task_id}")

            except Exception as e:
                logger.error(f"❌ Ошибка отправки предупреждения: {e}")