# states.py
from collections import defaultdict

# Состояния
STATE_NONE = "none"
STATE_NEW_TASK_TITLE = "new_task_title"
STATE_NEW_TASK_DESCRIPTION = "new_task_description"
STATE_NEW_TASK_DATE = "new_task_date"
STATE_NEW_TASK_TIME = "new_task_time"
STATE_NEW_TASK_PRIORITY = "new_task_priority"
STATE_NEW_TASK_CATEGORY = "new_task_category"
STATE_DELETE_TASK = "delete_task"
STATE_TASKS_MAKE_DONE = "tasks_make_done"
STATE_ADD_CATEGORY = "add_category"

# Хранилище состояний
user_states = defaultdict(dict)


def get_state(user_id):
    return user_states.get(user_id, {}).get("state", STATE_NONE)


def set_state(user_id, state, data=None):
    user_states[user_id] = {
        "state": state,
        "data": data or {}
    }


def get_data(user_id):
    return user_states.get(user_id, {}).get("data", {})


def clear_state(user_id):
    user_states.pop(user_id, None)