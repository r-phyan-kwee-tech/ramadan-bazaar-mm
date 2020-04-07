from db.shop import Shop
from db.user import User
from rabbit import Rabbit
from utils import str2bool


class MessengerUseCase:
    def __init__(self, payload, responder, db):
        super().__init__()

        self.payload = payload
        self.responder = responder
        self.db = db
        self.user = User(db)
        self.shop = Shop(db)

        self.recipient_id = ''
        self.quick_reply_payload = ''

    def handle_message(self):
        output = self.payload
        bot = self.responder
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                self.recipient_id = message['sender']['id']
                if message.get('message'):

                    bot.send_typing_on(self.recipient_id)
                    if message['message'].get('text') and message['message'].get('quick_reply') is None:
                        response_sent_text = "Hello"
                        bot.send_message(self.recipient_id, response_sent_text)

                    if message['message'].get('quick_reply'):
                        self.quick_reply_payload = message['message'].get('quick_reply').get('payload')
                        self.handle_quick_replies()

                if message.get("postback"):
                    initial_greetingb_bot = InitialConversationUseCase(self.recipient_id, bot)
                    if message["postback"]["payload"] == "GET_STARTED_PAYLOAD":
                        initial_greetingb_bot.send_initial_greeting()
                        users = self.user.select("WHERE sender_id = {0}".format(self.recipient_id))
                        if len(users) is 0:
                            self.user.insert({"sender_id": self.recipient_id})
                    else:
                        self.quick_reply_payload = message["postback"]["payload"]
                        self.handle_postback()
                bot.send_typing_off(self.recipient_id)

    def handle_quick_replies(self):

        bot = self.responder
        users = self.user.select("WHERE sender_id = {0}".format(self.recipient_id))
        if len(users) is not 0:
            current_user = users[0]
            fontselection_bot = FontSelectionUseCase(self.recipient_id, self.user, current_user, bot)
            fontselection_bot.handle_user_font_selection(self.quick_reply_payload)
            shop_selection_bot = ShopSelectionUseCase(self.recipient_id, self.shop, self.user, current_user, bot)
            shop_selection_bot.handle_shops_quick_reply(self.quick_reply_payload)

    def handle_postback(self):
        bot = self.responder
        users = self.user.select("WHERE sender_id = {0}".format(self.recipient_id))
        if len(users) is not 0:
            current_user = users[0]
            fontselection_bot = FontSelectionUseCase(self.recipient_id, self.user, current_user, bot)
            fontselection_bot.handle_user_font_selection(self.quick_reply_payload)
            shop_selection_bot = ShopSelectionUseCase(self.recipient_id, self.shop, self.user, current_user, bot)
            shop_selection_bot.handle_shops_quick_reply(self.quick_reply_payload)


class FontSelectionUseCase:

    def __init__(self, sender_id, user, current_user, bot):
        self.sender_id = sender_id
        self.bot = bot
        self.user = user
        self.current_user = current_user
        self.is_zawgyi = current_user.get('isZawgyi')
        self.FONT_SELECTION_PAYLOAD = "FONT_SELECTION_PAYLOAD"
        self.ZAW_GYI_PAYLOAD = "ZAW_GYI_PAYLOAD"
        self.UNICODE_PAYLOAD = "UNICODE_PAYLOAD"
        self.current_user = current_user
        self.SELECT_LOCATION_PAYLOAD = "SELECT_LOCATION_PAYLOAD"
        self.BROWSE_SHOPS = "BROWSE_SHOPS"
        self.AVAILABLE_MENUS="AVAILABLE_MENUS"
        self.ABOUT_US_PAYLOAD = "ABOUT_US_PAYLOAD"

        self.quick_reply_payload = ''
        self.EVENT_FONT_CHANGE = "အောက်မှာ မြင်ရတဲ့ စာသားလေးကိုနှိပ်ပြီး Font ရွေးပေးပါရှင်။"
        self.after_font_selection = "ကောင်းပါပြီ ဒါဆို အောက်က menuလေးတွေကို နှိပ်ပြီးကြည့်လို့ရပါပြီခင်ဗျာ။"

    def send_font_selection(self):
        is_zawgyi = False
        self.bot.send_quick_reply(self.sender_id, self.EVENT_FONT_CHANGE, self._font_selection_payload(), is_zawgyi)

    def handle_user_font_selection(self, payload):
        self.quick_reply_payload = payload
        if self.quick_reply_payload == self.FONT_SELECTION_PAYLOAD:
            self.bot.send_quick_reply(self.sender_id, self.EVENT_FONT_CHANGE, self._font_selection_payload(),
                                      self.is_zawgyi)

        if self.quick_reply_payload == self.ZAW_GYI_PAYLOAD:
            self.current_user["isZawgyi"] = True
            self.is_zawgyi = True
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            self.bot.send_quick_reply(self.sender_id, self.after_font_selection,
                                      self._after_font_selection_payload(self.is_zawgyi),
                                      self.is_zawgyi)

        if self.quick_reply_payload == self.UNICODE_PAYLOAD:
            self.current_user["isZawgyi"] = False
            self.is_zawgyi = False
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            self.bot.send_quick_reply(self.sender_id, self.after_font_selection,
                                      self._after_font_selection_payload(self.is_zawgyi),
                                      self.is_zawgyi)

    def _after_font_selection_payload(self, is_zawgyi):
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဝါဖြေပွဲ ကြည့်ရန်") if is_zawgyi else "ဝါဖြေပွဲ ကြည့်ရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_zawgyi.png",
                "payload": self.BROWSE_SHOPS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဘာစားစရာရလဲကြည့်မယ်") if is_zawgyi else "ဘာစားစရာရလဲကြည့်မယ်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.AVAILABLE_MENUS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("တည်နေရာရွေးရန်") if is_zawgyi else "တည်နေရာရွေးရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.SELECT_LOCATION_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ကျွန်တော်တို့အကြောင်း") if is_zawgyi else "ကျွန်တော်တို့အကြောင်း",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.ABOUT_US_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဖောင့်ပြန်ရွေးရန်") if is_zawgyi else "ဖောင့်ပြန်ရွေးရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.FONT_SELECTION_PAYLOAD
            }

        ]

    def _font_selection_payload(self):
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("မြန်မာစာ"),
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_zawgyi.png",
                "payload": self.ZAW_GYI_PAYLOAD
            },
            {
                "content_type": "text",
                "title": "မြန်မာစာ",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.UNICODE_PAYLOAD
            }

        ]


class ShopSelectionUseCase:
    def __init__(self, sender_id, shop, user, current_user, bot):
        self.sender_id = sender_id
        self.bot = bot
        self.shop = shop
        self.page_num = current_user.get('current_shop_page')
        self.page_size = 10
        self.user = user
        self.current_user = current_user

        self.is_zawgyi = current_user.get('isZawgyi')
        self.SELECT_LOCATION_PAYLOAD = "SELECT_LOCATION_PAYLOAD"
        self.BROWSE_SHOPS = "BROWSE_SHOPS"
        self.NEXT_SHOPS = "NEXT_SHOPS"
        self.VIEW_SHOP="VIEW_SHOP"
        self.AVAILABLE_MENUS="AVAILABLE_MENUS"
        self.ABOUT_US_PAYLOAD = "ABOUT_US_PAYLOAD"
        self.FONT_SELECTION_PAYLOAD = "FONT_SELECTION_PAYLOAD"
        self.EXIT_SHOPS = "EXIT_SHOPS"
        self.after_exit_shops = "ကောင်းပါပြီ ဒါဆို အောက်က သင်ကြည့်လိုတဲ့ လုပ်ဆောင်လိုတဲ့ ခလုတ်လေးတွေကိုနှိပ်လို့ရပါပြီခင်ဗျာ။ "
        self.browse_shops_end = "ဆိုင်တွေအားလုံးကြည့်လိုတော့ကုန်သွားပြီ ဒါဆို နောက်တခေါက်ပြန်ကြည့်ဖို့ အောက်က ခလုတ်လေးတွေကိုနှိပ်လို့ရပါပြီခင်ဗျာ။ "

    def handle_shops_quick_reply(self, payload):
        if payload == self.BROWSE_SHOPS:
            self.current_user["current_shop_page"] = 1
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            shops = self.shop.select(None, self.page_num, self.page_size)
            if len(shops) is not 0:
                self.bot.send_generic_reply(self.sender_id, self._generate_shops(shops, self.is_zawgyi), self.is_zawgyi)

        if payload == self.AVAILABLE_MENUS:
            self.current_user["current_shop_page"] = 1
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            shops = self.shop.select(None, self.page_num, self.page_size)
            if len(shops) is not 0:
                self.bot.send_generic_reply(self.sender_id, self._generate_shops(shops, self.is_zawgyi), self.is_zawgyi)

        if payload == self.NEXT_SHOPS:

            self.page_num = self.current_user.get('current_shop_page') + 1

            shops = self.shop.select(None, self.page_num, self.page_size)
            self.current_user["current_shop_page"] = self.page_num
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))

            if len(shops) is not 0:

                self.bot.send_generic_reply(self.sender_id, self._generate_shops(shops, self.is_zawgyi), self.is_zawgyi)
            else:

                self.current_user["current_shop_page"] = 1
                self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))

                self.bot.send_quick_reply(self.sender_id, self.browse_shops_end,
                                          self._after_shop_selection_exit(self.is_zawgyi),
                                          self.is_zawgyi)
        if payload == self.EXIT_SHOPS:
            self.current_user["current_shop_page"] = 1
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            self.bot.send_quick_reply(self.sender_id, self.after_exit_shops,
                                      self._after_shop_selection_exit(self.is_zawgyi),
                                      self.is_zawgyi)

    def _after_shop_selection_exit(self, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဝါဖြေပွဲ ကြည့်ရန်") if is_zawgyi else "ဝါဖြေပွဲ ကြည့်ရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_zawgyi.png",
                "payload": self.BROWSE_SHOPS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဘာစားစရာရလဲကြည့်မယ်") if is_zawgyi else "ဘာစားစရာရလဲကြည့်မယ်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.AVAILABLE_MENUS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("တည်နေရာရွေးရန်") if is_zawgyi else "တည်နေရာရွေးရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.SELECT_LOCATION_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ကျွန်တော်တို့အကြောင်း") if is_zawgyi else "ကျွန်တော်တို့အကြောင်း",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.ABOUT_US_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဖောင့်ပြန်ရွေးရန်") if is_zawgyi else "ဖောင့်ပြန်ရွေးရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.FONT_SELECTION_PAYLOAD
            }

        ]

    def _generate_shops(self, shops, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)

        return [{
            "title": Rabbit.uni2zg(str(shop.get("name_uni"))) if is_zawgyi else str(shop.get("name_uni")),
            "image_url": "http://source.unsplash.com/NEqPK_bF3HQ",
            "subtitle": Rabbit.uni2zg(str(shop.get("description"))) if is_zawgyi else shop.get("description"),
            "default_action": {
                "type": "web_url",
                "url": "https://msglocation.github.io",
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "postback",
                    "title": Rabbit.uni2zg("ဘာရလဲကြည့်မယ်") if is_zawgyi else "ဘာရလဲကြည့်မယ်",
                    "payload": self.VIEW_SHOP
                },
                {
                    "type": "postback",
                    "title": Rabbit.uni2zg("ဆိုင်တွေထပ်ကြည့်မယ်") if is_zawgyi else "ဆိုင်တွေထပ်ကြည့်မယ်",
                    "payload": self.NEXT_SHOPS
                },
                {
                    "type": "postback",
                    "title": Rabbit.uni2zg("မကြည့်တော့ဘူး") if is_zawgyi else "မကြည့်တော့ဘူး",
                    "payload": self.EXIT_SHOPS
                }
            ]
        } for shop in shops]


class InitialConversationUseCase:

    def __init__(self, sender_id, bot):
        self.sender_id = sender_id
        self.bot = bot
        self.MSG_INITIAL_GREETING = Rabbit.uni2zg(
            "အစ်စလာမို့ အာလိုင်းကွန်း (Assalamualaikum)" \
            "Ramadan Bazaar Myanmar မှကြိုဆိုပါတယ်ခင်ဗျာ။ ပထမဦးစွာ အောက်မှာမြင်ရတဲ့ Font လေးရွေးပေးပါအုံး။")
        self.ZAW_GYI_PAYLOAD = "ZAW_GYI_PAYLOAD"
        self.UNICODE_PAYLOAD = "UNICODE_PAYLOAD"

    def send_initial_greeting(self):
        is_zawgyi = False
        self.bot.send_quick_reply(self.sender_id, self.MSG_INITIAL_GREETING, self._font_selection_payload(), is_zawgyi)

    def _font_selection_payload(self):
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("မြန်မာစာ"),
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_zawgyi.png",
                "payload": self.ZAW_GYI_PAYLOAD
            },
            {
                "content_type": "text",
                "title": "မြန်မာစာ",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.UNICODE_PAYLOAD
            }

        ]
