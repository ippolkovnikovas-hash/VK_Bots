# keyboards/keyboards.py
def get_main_keyboard():
    """Главная клавиатура."""
    from vk_api.keyboard import VkKeyboard, VkKeyboardColor

    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('📝 Новая задача', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('📋 Задачи', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('📅 Сегодня', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('📊 Статистика', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button('❓ Помощь', color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()