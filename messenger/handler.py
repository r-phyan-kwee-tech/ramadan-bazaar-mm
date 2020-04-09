import json
import os

import tornado

from bot.messenger import MessengerBot
from messenger.usecase import MessengerUseCase
from server import BaseHandler


class MessengerHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("hub.mode") == "subscribe" and self.get_argument("hub.challenge"):
            if not self.get_argument("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
                return self.send_error({}, 403)

            return self.write(self.get_argument("hub.challenge"))

    @tornado.gen.coroutine
    def post(self):

        bot = MessengerBot(os.environ['VERIFY_TOKEN'])

        output = json.loads(self.request.body)
        messenger_uc = MessengerUseCase(output, bot, self.application.db)
        messenger_uc.handle_message()
        self.set_default_headers()
        self.write_json({"result": True, "listing": []})

# /listings/ping
