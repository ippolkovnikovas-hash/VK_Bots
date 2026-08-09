import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import VK_GROUP_TOKEN
from handlers import handle_message


def main():
    vk_session = vk_api.VkApi(token=VK_GROUP_TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    print("Бот запущен и слушает события Long Poll...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            text = event.text or ""
            print(f"Сообщение от {user_id}: {text}")
            try:
                handle_message(vk, user_id, text)
            except Exception as exc:
                print(f"Ошибка обработки сообщения: {exc}")


if __name__ == "__main__":
    main()
