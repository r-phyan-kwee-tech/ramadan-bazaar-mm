import json
import os

import jwt
from tornado import httpclient
from tornado.httputil import url_concat

from rabbit import Rabbit
from utils import str2bool


class MessengerBot:

    def __init__(self, verify_token):
        super().__init__()

        # Initialising page token
        self.page_token = verify_token

    def send_message(self, recipient_id, message_text):
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",
                                           headers=headers, body=data)

    def send_typing_on(self, recipient_id):
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "sender_action": 'typing_on'
        })
        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",
                                           headers=headers,
                                           body=data)

    def send_typing_off(self, recipient_id):
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "sender_action": 'typing_off'
        })
        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",

                                           headers=headers,
                                           body=data)

    def send_quick_reply(self, recipient_id, message, arr_quick_reply_response, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": Rabbit.uni2zg(message) if is_zawgyi else message,
                "quick_replies": arr_quick_reply_response
            }

        })
        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",
                                           headers=headers,
                                           body=data)

    def send_generic_reply(self, recipient_id, arr_quick_reply_response, is_zawgyi):
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": arr_quick_reply_response
                    }
                }
            }

        })
        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",

                                           headers=headers,
                                           body=data)

    def send_yes_no_quick_reply(self, recipient_id, message, arr_quick_reply_response, is_zawgyi):
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": Rabbit.uni2zg(message) if is_zawgyi else message,
                "quick_replies": arr_quick_reply_response
            }

        })
        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",
                                           params=params,
                                           headers=headers,
                                           body=data)

    def send_greeting_quick_reply(self, recipient_id, message, arr_quick_reply_response):
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message,
                "quick_replies": arr_quick_reply_response
            }

        })
        httpclient.AsyncHTTPClient().fetch("https://graph.facebook.com/v6.0/me/messages", method="POST",
                                           params=params,
                                           headers=headers,
                                           body=data)

    def send_location_reply(self, recipient_id, message, is_zawgyi, page_id, page_recipient_id):
        is_zawgyi = str2bool(is_zawgyi)
        params = {
            "access_token": self.page_token
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "text": Rabbit.uni2zg(message) if is_zawgyi else message,
                        "template_type": "button",
                        "buttons": [
                            {
                                "type": "web_url",
                                "title": Rabbit.uni2zg(
                                    "လက်ရှိနေရာ ပို့ပေးမယ်") if is_zawgyi else "လက်ရှိနေရာ ပို့ပေးမယ်",
                                "url": "https://msglocation.github.io/?verification_token=" + str(
                                    jwt.encode(
                                        {"recepient_id": recipient_id, "post_back_url": os.getenv("MSG_POST_BACK_URL"),
                                         "page_id": page_id, "page_recipient_id": page_recipient_id},
                                        os.getenv("JWT_KEY"),
                                        algorithm='HS256')).replace("b'", "").replace("'",
                                                                                      "")

                            },
                            {
                                "type": "postback",
                                "title": Rabbit.uni2zg("မပို့တော့ဘူး") if is_zawgyi else "မပို့တော့ဘူး",
                                "payload": "NO_LOCATION_PAYLOAD",
                            }
                        ]
                    }
                }
            }

        })

        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",
                                           headers=headers, body=data)
