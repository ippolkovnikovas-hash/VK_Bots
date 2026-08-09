# 🤖 VK Task Manager Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![VK API](https://img.shields.io/badge/VK-API-0077FF?style=for-the-badge&logo=vk&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**Умный бот для управления задачами прямо в ВКонтакте!** 🚀

[👤 Попробовать бота](https://vk.com/club240287658) •
[📝 Сообщить о проблеме](https://github.com/ваш-username/vk-task-bot/issues) •
[⭐ Поставить звезду](https://github.com/ваш-username/vk-task-bot)

</div>

---

## 📋 Оглавление

- [Возможности](#-возможности)
- [Демонстрация](#-демонстрация)
- [Установка](#-установка)
- [Команды](#-команды)
- [Структура проекта](#-структура-проекта)
- [Технологии](#-технологии)
- [Скриншоты](#-скриншоты)
- [Вклад в проект](#-вклад-в-проект)
- [Лицензия](#-лицензия)
- [Контакты](#-контакты)

---

## ✨ Возможности

<table>
<tr>
<td width="50%" valign="top">

### 📝 Управление задачами
- ✅ Создание задач с дедлайном
- 📄 Добавление описания
- ⏰ Установка времени выполнения
- 🏷️ Категории для группировки
- 🎯 Приоритеты (Высокий / Средний / Низкий)

</td>
<td width="50%" valign="top">

### ⏰ Напоминания
- 🔔 Автоматические напоминания
- 📅 Уведомление за день до дедлайна
- ⏱️ Напоминание в день выполнения
- 🔄 Настраиваемый интервал проверки

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 Статистика
- 📈 Продуктивность пользователя
- 📊 Статистика по приоритетам
- 📅 Распределение по дням недели
- ⏱️ Среднее время выполнения

</td>
<td width="50%" valign="top">

### 🔧 Управление
- ✅ Изменение статуса задачи
- 🗑️ Удаление выполненных задач
- 🔍 Просмотр задач (все / сегодня / неделя)
- ⚠️ Отображение просроченных задач

</td>
</tr>
</table>

---

## 🎬 Демонстрация

### Создание задачи

```
👤 Пользователь: newtask
🤖 Бот: 📝 Введите название задачи:
👤 Пользователь: Купить продукты
🤖 Бот: 📄 Введите описание задачи (или '-' чтобы пропустить):
👤 Пользователь: Молоко, хлеб, яйца
🤖 Бот: 📅 Введите дату выполнения (ДД.ММ.ГГГГ):
👤 Пользователь: 20.07.2026
🤖 Бот: ⏰ Введите время выполнения (ЧЧ:ММ) или '-' чтобы пропустить:
👤 Пользователь: 18:00
🤖 Бот: ✅ Задача создана!
```

### Просмотр задач

```
👤 Пользователь: today
🤖 Бот: 📅 Задачи на сегодня:
⬜ Купить продукты - 20.07.2026 18:00 🟡
⬜ Встреча с командой - 20.07.2026 14:00 🔴
💡 Введите номер задачи, чтобы изменить её статус.
```

### Статистика

```
👤 Пользователь: stats
🤖 Бот: 📈 ПРОДВИНУТАЯ СТАТИСТИКА

📊 ОБЩАЯ ИНФОРМАЦИЯ:
• Всего задач: 25
• Выполнено: 18 (72%)
• Ожидает: 7
• Просрочено: 2
• На сегодня: 3

📊 ПРОДУКТИВНОСТЬ: 85%
⭐ Отлично!
```

---

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-username/vk-task-bot.git
cd vk-task-bot
```

### 2. Создание виртуального окружения

<details>
<summary><b>Windows</b></summary>

```bash
python -m venv env
env\Scripts\activate
```

</details>

<details>
<summary><b>Linux / macOS</b></summary>

```bash
python3 -m venv env
source env/bin/activate
```

</details>

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

```bash
# Копируем файл с настройками
cp .env.example .env

# Редактируем .env, добавляем BOT_TOKEN
nano .env
```

Пример `.env`:

```env
BOT_TOKEN=ваш_токен_сообщества
DB_PATH=database/database.db
LOG_LEVEL=INFO
MAX_TASKS_PER_USER=100
DEFAULT_PRIORITY=2
ENABLE_NOTIFICATIONS=true
REMINDER_CHECK_INTERVAL=60
TASKS_PER_PAGE=10
```

> ⚠️ **Важно:** файл `.env` содержит секретные данные и уже добавлен в `.gitignore` — никогда не коммитьте его в репозиторий.

### 5. Запуск

```bash
python main.py
```

---

## 📱 Команды

| Команда | Описание | Пример |
|---|---|---|
| `start` | Начать работу с ботом | `start` |
| `newtask` | Создать новую задачу | `newtask` |
| `tasks` | Показать последние 10 задач | `tasks` |
| `today` | Задачи на сегодня | `today` |
| `week` | Задачи на неделю | `week` |
| `overdue` | Просроченные задачи | `overdue` |
| `completed` | Выполненные задачи | `completed` |
| `delete` | Удалить задачу | `delete` |
| `stats` | Статистика продуктивности | `stats` |
| `category` | Создать категорию | `category` |
| `help` | Справка по командам | `help` |

---

## 📁 Структура проекта

```
vk-task-bot/
├── main.py                 # Главный файл бота
├── config.py               # Конфигурация
├── models.py               # Модели базы данных
├── states.py                # Состояния пользователей
├── scheduler.py             # Планировщик напоминаний
├── loader.py                 # Загрузчик
├── requirements.txt          # Зависимости
├── .env.example              # Пример конфигурации
├── .gitignore                # Игнорируемые файлы
├── README.md                 # Документация
│
├── handlers/                 # Обработчики команд
│   ├── __init__.py
│   ├── task_handlers.py       # Задачи
│   ├── stat_handlers.py       # Статистика
│   └── category_handlers.py   # Категории
│
├── utils/                     # Утилиты
│   ├── __init__.py
│   └── helpers.py              # Вспомогательные функции
│
├── keyboards/                 # Клавиатуры
│   └── keyboards.py
│
└── database/                  # База данных
    └── database.db
```

---

## 🛠️ Технологии

<div align="center">

| Технология | Описание |
|---|---|
| 🐍 **Python 3.8+** | Основной язык разработки |
| 📱 **VK API** | Взаимодействие с ВКонтакте |
| 🗃️ **Peewee** | ORM для работы с SQLite |
| 📊 **SQLite** | База данных |
| 🔐 **python-dotenv** | Управление переменными окружения |

</div>

---

## 📸 Скриншоты

<details>
<summary><b>👀 Нажмите, чтобы посмотреть скриншоты</b></summary>

**Главное меню**
![Главное меню](https://via.placeholder.com/400x300?text=%D0%93%D0%BB%D0%B0%D0%B2%D0%BD%D0%BE%D0%B5+%D0%BC%D0%B5%D0%BD%D1%8E)

**Создание задачи**
![Создание задачи](https://via.placeholder.com/400x300?text=%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5+%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8)

**Список задач**
![Список задач](https://via.placeholder.com/400x300?text=%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA+%D0%B7%D0%B0%D0%B4%D0%B0%D1%87)

**Статистика**
![Статистика](https://via.placeholder.com/400x300?text=%D0%A1%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0)

</details>

---

## 🤝 Вклад в проект

Мы приветствуем вклад в проект! Вот как вы можете помочь:

1. 🍴 Форкните репозиторий
2. 🌿 Создайте ветку для новой функции:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. 💻 Внесите изменения и сделайте коммит:
   ```bash
   git commit -m "Добавлена новая фича"
   ```
4. 📤 Отправьте изменения:
   ```bash
   git push origin feature/amazing-feature
   ```
5. 🔄 Создайте Pull Request

---

## 📝 Лицензия

Этот проект распространяется под лицензией **MIT**. Подробнее см. в файле [LICENSE](LICENSE).

```
MIT License

Copyright (c) 2026 Ваше Имя

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...
```

Полный текст лицензии — в файле `LICENSE`.

---

## 📞 Контакты

<div align="center">

**Автор:** Ваше Имя

[![VK](https://img.shields.io/badge/VK-0077FF?style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/ваш_профиль)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ваш-username)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/ваш_телеграм)

</div>

<div align="center">

⭐ **Если вам понравился проект, поставьте звезду на GitHub!** ⭐

Сделано с ❤️ для сообщества VK

</div>
