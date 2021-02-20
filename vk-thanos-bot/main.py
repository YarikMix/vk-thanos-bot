# -*- coding: utf-8 -*-
import random
import time

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import yaml

from quotes import quotes

with open("config.yaml") as ymlFile:
    config = yaml.load(ymlFile.read(), Loader=yaml.Loader)


class Bot:
    def __init__(self):
        authorize = vk_api.VkApi(token=config["group"]["group_token"])
        self.longpoll = VkBotLongPoll(
            authorize,
            group_id=config["group"]["group_id"]
        )

        self.bot = authorize.get_api()

    def destroy(self, chat_id):
        # Создаём интригу
        time.sleep(random.randint(1, 5))

        self.bot.messages.send(
            chat_id=chat_id,
            message=random.choice(quotes),
            random_id=get_random_id()
        )

        # Создаём интригу
        time.sleep(random.randint(1, 30))

        # Получаем участников беседы
        chat_members = self.bot.messages.getConversationMembers(
            peer_id=2000000000 + chat_id,
            group_id=config["group"]["group_id"],
        )["items"]

        users = []

        # Не трогаем админов и ботов
        for user in chat_members:
            if user["member_id"] > 0 and "is_admin" not in user:
                users.append(user)

        # Начинаем выборку
        for _ in range(len(users) // 2):
            user = random.choice(users)
            self.bot.messages.removeChatUser(
                chat_id=chat_id,
                user_id=user["member_id"]
            )

            users.remove(user)

        print("Success")

    def run(self):
        print("Начинаю мониторинг сообщений...")

        # Отслеживаем каждое событие в беседе
        while True:
            try:
                for event in self.longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get("text") != "":
                        if event.message.get("text").lower() == "танос":
                            self.destroy(event.chat_id)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    VkBot = Bot()
    VkBot.run()