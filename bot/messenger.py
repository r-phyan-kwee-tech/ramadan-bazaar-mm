import json

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

    def send_location_reply(self, recipient_id, message):
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
                "quick_replies": [
                    {
                        "content_type": "location",
                        "title": "Location",
                        "payload": "LOCATION_PAYLOAD"
                    }, {
                        "content_type": "text",
                        "title": "Nope",
                        "payload": "LOCATION_NEGATIVE_PAYLOAD"
                    }
                ]
            }

        })
        url = url_concat("https://graph.facebook.com/v6.0/me/messages", params)
        httpclient.AsyncHTTPClient().fetch(url, method="POST",
                                           headers=headers, body=data)
