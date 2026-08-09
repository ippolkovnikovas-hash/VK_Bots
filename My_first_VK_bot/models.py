# models.py
from peewee import *
import datetime
from config import DATE_FORMAT, DATETIME_FORMAT, PRIORITY_NAMES

db = SqliteDatabase("database/database.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    first_name = CharField()
    last_name = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    last_active = DateTimeField(default=datetime.datetime.now)


class Task(BaseModel):
    task_id = AutoField()
    user = ForeignKeyField(User, backref="tasks")
    title = CharField()
    description = TextField(null=True)
    due_date = DateField()
    due_time = TimeField(null=True)
    is_done = BooleanField(default=False)
    priority = IntegerField(default=2)
    created_at = DateTimeField(default=datetime.datetime.now)
    completed_at = DateTimeField(null=True)

    def __str__(self):
        priority_icon = "🔴" if self.priority == 1 else "🟡" if self.priority == 2 else "🟢"
        check = "✅" if self.is_done else "⬜"
        date_str = self.due_date.strftime(DATE_FORMAT)
        if self.due_time:
            date_str += f" {self.due_time.strftime('%H:%M')}"

        return f"{self.task_id}. {check} {self.title} - {date_str} {priority_icon}"

    def get_full_info(self):
        status = "✅ Выполнена" if self.is_done else "⏳ Ожидает выполнения"
        date_str = self.due_date.strftime(DATE_FORMAT)
        if self.due_time:
            date_str += f" {self.due_time.strftime('%H:%M')}"

        return f"""
📌 Задача #{self.task_id}
Название: {self.title}
Приоритет: {PRIORITY_NAMES.get(self.priority, "🟡 Средний")}
Статус: {status}
Дедлайн: {date_str}
Описание: {self.description or "Без описания"}
Создана: {self.created_at.strftime(DATE_FORMAT)}
"""

    def mark_done(self):
        self.is_done = True
        self.completed_at = datetime.datetime.now()
        self.save()


class Category(BaseModel):
    user = ForeignKeyField(User, backref="categories")
    name = CharField()
    color = CharField(default="#FFFFFF")

    class Meta:
        indexes = (
            (('user', 'name'), True),
        )


class TaskCategory(BaseModel):
    task = ForeignKeyField(Task, backref="categories")
    category = ForeignKeyField(Category, backref="tasks")

    class Meta:
        indexes = (
            (('task', 'category'), True),
        )


class Reminder(BaseModel):
    task = ForeignKeyField(Task, backref="reminders")
    reminder_time = DateTimeField()
    is_sent = BooleanField(default=False)


def create_models():
    db.create_tables([User, Task, Category, TaskCategory, Reminder])