# -*- coding: utf-8 -*-
import random, time

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import yaml

from quotes import quotes

with open("config.yaml") as ymlFile:
    config = yaml.load(ymlFile.read(), Loader=yaml.Loader)


class Bot:
    def auth(self):
        self.authorize = vk_api.VkApi(token=config["group"]["group_token"])
        self.longpoll = VkBotLongPoll(
            self.authorize,
            group_id=config["group"]["group_id"]
        )

        self.upload = vk_api.VkUpload(self.authorize)
        self.bot = self.authorize.get_api()

        vk_session = vk_api.VkApi(
            token=config["access_token"]["token"]
        )

        self.vk = vk_session.get_api()

    def destroy(self):
        # Создаём интригу
        time.sleep(random.randint(1, 5))

        self.bot.messages.send(
            chat_id=self.chat_id,
            message=random.choice(quotes),
            random_id=get_random_id()
        )

        # Создаём интригу
        time.sleep(random.randint(1, 30))

        # Получаем участников беседы
        chat_members = self.bot.messages.getConversationMembers(
            peer_id=2000000000 + self.chat_id,
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
                chat_id=self.chat_id,
                user_id=user["member_id"]
            )

            users.remove(user)

        print("Success")

    def run(self):
        self.auth()
        
        print("Начинаю мониторинг сообщений...")

        # Отслеживаем каждое событие в беседе
        try:
            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get("text") != "":
                    self.chat_id = event.chat_id
                    if event.message.get("text").lower() == "танос":
                        self.destroy()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    VkBot = Bot()
    VkBot.run()