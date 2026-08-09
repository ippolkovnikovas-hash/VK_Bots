from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def main_keyboard() -> str:
    """Возвращает JSON основной клавиатуры бота."""
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button("Привет", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Помощь", color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button("Время", color=VkKeyboardColor.POSITIVE)

    return keyboard.get_keyboard()
