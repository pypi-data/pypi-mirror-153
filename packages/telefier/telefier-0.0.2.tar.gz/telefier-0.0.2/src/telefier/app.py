#!/usr/bin/env python

import logging
from telethon.sync import TelegramClient


class Telefier:
    def __init__(self, api_id: str, api_hash: str, token: str):
        self.username = username
        self.api_id = api_id
        self.api_hash = api_hash
        self.token = token

    def connect(self):
        self.client = TelegramClient("telefier", self.api_id, self.api_hash)
        self.client.start(bot_token=self.token)
        self.client.connect()

    def notify(self, username, message):
        self.client.send_message(username, message)
