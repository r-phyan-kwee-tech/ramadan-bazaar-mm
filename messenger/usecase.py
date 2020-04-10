import decimal

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
        self.page_id = ''
        self.page_sender_id = ''
        self.page_recipient_id = ''
        self.sent_text = ''
        self.recipient_reaction = None
        self.latitude = 0.0
        self.longitude = 0.0
        self.recipient_id = ''
        self.quick_reply_payload = ''

    def handle_message(self):
        output = self.payload
        bot = self.responder
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                self.recipient_id = message['sender']['id']
                self.page_id = event.get("id")
                self.page_sender_id = self.recipient_id
                self.page_recipient_id = message['recipient']['id']

                if message.get('message'):

                    bot.send_typing_on(self.recipient_id)
                    if message['message'].get('text') and message['message'].get('quick_reply') is None:
                        self.sent_text = message['message'].get('text')
                        self.handle_text_input()

                    if message['message'].get('quick_reply'):
                        self.quick_reply_payload = message['message'].get('quick_reply').get('payload')
                        self.handle_quick_replies()
                    if message["message"].get("attachments"):
                        if message["message"].get("attachments")[0].get("type") == 'location':
                            self.latitude = message["message"]["attachments"][0]["payload"]["coordinates"][
                                "lat"]
                            self.longitude = message["message"]["attachments"][0]["payload"]["coordinates"][
                                "long"]
                            self.handle_attachment()
                        else:
                            response_sent_text = "Oops I think I am not good enough to handle this request thousand apologies."
                            bot.send_message(self.recipient_id, response_sent_text)
                if message.get("reaction"):
                    self.recipient_reaction = message.get("reaction").get("reaction")
                    self.handle_reaction()
                if message.get("postback"):
                    initial_greetingb_bot = InitialConversationUseCase(self.recipient_id, bot)
                    if message["postback"]["payload"] == "GET_STARTED_PAYLOAD":
                        initial_greetingb_bot.send_initial_greeting()
                        users = self.user.select("WHERE public.user.sender_id = {0}".format(self.recipient_id))
                        if len(users) is 0:
                            self.user.insert({"sender_id": self.recipient_id})
                    else:
                        self.quick_reply_payload = message["postback"]["payload"]
                        self.handle_postback()
                bot.send_typing_off(self.recipient_id)

    def handle_text_input(self):
        bot = self.responder
        users = self.user.select("WHERE public.user.sender_id = {0}".format(self.recipient_id))
        if len(users) is not 0:
            current_user = users[0]
            reaction_bot = TextInputResponseUseCase(self.recipient_id, self.recipient_reaction, current_user, bot)
            reaction_bot.handle_text_response()

    def handle_reaction(self):
        bot = self.responder
        users = self.user.select("WHERE public.user.sender_id = {0}".format(self.recipient_id))
        if len(users) is not 0:
            current_user = users[0]
            reaction_bot = ReactionResponseUseCase(self.recipient_id, self.recipient_reaction, current_user, bot)
            reaction_bot.handle_reaction()

    def handle_attachment(self):
        bot = self.responder
        users = self.user.select("WHERE public.user.sender_id = {0}".format(self.recipient_id))
        if len(users) is not 0:
            current_user = users[0]
            current_user['lat'] = self.latitude
            current_user['lon'] = self.longitude
            self.user.update(current_user, " public.user.sender_id = {0}".format(self.recipient_id))
            updated_users = self.user.select("WHERE public.user.sender_id = {0}".format(self.recipient_id))
            current_user = updated_users[0]
            location_selection_bot = LocationBaseShopSelectionUseCase(self.recipient_id, self.shop, self.user,
                                                                      current_user, bot)
            location_selection_bot.handle_initial_location_reply()
        pass

    def handle_quick_replies(self):

        bot = self.responder
        users = self.user.select("WHERE public.user.sender_id = {0}".format(self.recipient_id))
        if len(users) is not 0:
            current_user = users[0]
            fontselection_bot = FontSelectionUseCase(self.recipient_id, self.user, current_user, bot, self.page_id,
                                                     self.page_recipient_id)
            fontselection_bot.handle_user_font_selection(self.quick_reply_payload)
            shop_selection_bot = ShopSelectionUseCase(self.recipient_id, self.shop, self.user, current_user, bot)
            shop_selection_bot.handle_shops_quick_reply(self.quick_reply_payload)

    def handle_postback(self):
        bot = self.responder
        users = self.user.select("WHERE public.user.sender_id = {0}".format(self.recipient_id))
        if len(users) is not 0:
            current_user = users[0]
            fontselection_bot = FontSelectionUseCase(self.recipient_id, self.user, current_user, bot, self.page_id,
                                                     self.page_recipient_id)
            fontselection_bot.handle_user_font_selection(self.quick_reply_payload)
            shop_selection_bot = ShopSelectionUseCase(self.recipient_id, self.shop, self.user, current_user, bot)
            shop_selection_bot.handle_shops_quick_reply(self.quick_reply_payload)
            location_selection_bot = LocationBaseShopSelectionUseCase(self.recipient_id, self.shop, self.user,
                                                                      current_user, bot)
            location_selection_bot.handle_location_base_reply(self.quick_reply_payload)


class TextInputResponseUseCase:
    def __init__(self, sender_id, reaction, current_user, bot):
        self.sender_id = sender_id
        self.bot = bot
        self.reaction = reaction
        self.current_user = current_user
        self.is_zawgyi = current_user.get("iszawgyi")
        self.BROWSE_SHOPS = "BROWSE_SHOPS"
        self.SELECT_LOCATION_PAYLOAD = "SELECT_LOCATION_PAYLOAD"
        self.ABOUT_US_PAYLOAD = "ABOUT_US_PAYLOAD"
        self.FONT_SELECTION_PAYLOAD = "FONT_SELECTION_PAYLOAD"

        self.after_text_input_received_text = "ဆက်သွယ်ပေးတာကျေးဇူးတင်ပါတယ်ခင်ဗျာ Ramadan Bazaar Myanmar Page တွင် အခမဲ့ ဝါဖြေပွဲရောင်းချလိုပါက ဒီဖုန်းနံပါတ် 09764328010 ကိုဆက်သွယ်ပေးပါခင်ဗျာ။"

    def handle_text_response(self):
        self.bot.send_quick_reply(self.sender_id, self.after_text_input_received_text,
                                  self._after_text_input_received(self.is_zawgyi), self.is_zawgyi)

    def _after_text_input_received(self, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဆိုင်တွေကိုကြည့်မယ်") if is_zawgyi else "ဆိုင်တွေကိုကြည့်မယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_fork_knife.png",
                "payload": self.BROWSE_SHOPS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("အနီးနားမှာရှာမယ်") if is_zawgyi else "အနီးနားမှာရှာမယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_location.png",
                "payload": self.SELECT_LOCATION_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ကျွန်တော်တို့အကြောင်း") if is_zawgyi else "ကျွန်တော်တို့အကြောင်း",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_info.png",
                "payload": self.ABOUT_US_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဖောင့်ပြန်ရွေးရန်") if is_zawgyi else "ဖောင့်ပြန်ရွေးရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.FONT_SELECTION_PAYLOAD
            }

        ]


class ReactionResponseUseCase:
    def __init__(self, sender_id, reaction, current_user, bot):
        self.sender_id = sender_id
        self.bot = bot
        self.reaction = reaction
        self.current_user = current_user
        self.is_zawgyi = current_user.get("iszawgyi")

    def handle_reaction(self):

        if self.reaction == 'wow':
            self.bot.send_message(self.sender_id, "တကယ်အံသြ တယ်ဆိုရင် ကျေးဇူးတင်ပါတယ်ဗျာ။", self.is_zawgyi)
        if self.reaction == 'like':
            self.bot.send_message(self.sender_id, "တကယ်ကြိုက်တယ်ဆိုတာသိရတော့လည်း ပျော်တာပေါ့", self.is_zawgyi)
        if self.reaction == 'love':
            self.bot.send_message(self.sender_id, "အသဲလေးတွေပေးတယ်ဆိုတော့ ကြွေတာပေါ့", self.is_zawgyi)
        if self.reaction == 'angry':
            self.bot.send_message(self.sender_id, "ဘာများအဆင်မပြေတာရှိလို့ လဲ ဗျာ ကျနော့် ကိုပြောပါအုန်းဗျ။",
                                  self.is_zawgyi)
        if self.reaction == 'sad':
            self.bot.send_message(self.sender_id, "ဝမ်းမနည်းပါနဲ့ဗျာ အဆင်မပြေတာတွေ အဆင်ပြေသွားမှာပါဗျာ။",
                                  self.is_zawgyi)
        if self.reaction == 'other':
            self.bot.send_message(self.sender_id, "react လေးတွေလာပေးတယ်ပေါ့", self.is_zawgyi)


class LocationBaseShopSelectionUseCase:
    def __init__(self, sender_id, shop, user, current_user, bot):
        self.sender_id = sender_id
        self.bot = bot
        self.shop = shop
        self.page_num = current_user.get('current_shop_page')
        self.page_size = 10
        self.user = user
        self.current_user = current_user
        self.latitude = current_user.get("lat")
        self.longitude = current_user.get("lon")

        self.is_zawgyi = current_user.get('iszawgyi')
        self.SELECT_LOCATION_PAYLOAD = "SELECT_LOCATION_PAYLOAD"
        self.BROWSE_LOCATION_SHOPS = "BROWSE_LOCATION_SHOPS"
        self.BROWSE_SHOPS = "BROWSE_SHOPS"
        self.NEXT_LOCATION_SHOPS = "NEXT_LOCATION_SHOPS"
        self.VIEW_LOCATION_SHOP = "VIEW_LOCATION_SHOP"
        self.AVAILABLE_MENUS = "AVAILABLE_MENUS"
        self.ABOUT_US_PAYLOAD = "ABOUT_US_PAYLOAD"
        self.FONT_SELECTION_PAYLOAD = "FONT_SELECTION_PAYLOAD"
        self.EXIT_SHOPS = "EXIT_SHOPS"

        self.after_exit_shops = "ကောင်းပါပြီ ဒါဆို အောက်က သင်ကြည့်လိုတဲ့ လုပ်ဆောင်လိုတဲ့ ခလုတ်လေးတွေကိုနှိပ်လို့ရပါပြီခင်ဗျာ။ "
        self.browse_shops_end = "ဆိုင်တွေအားလုံးကြည့်လိုတော့ကုန်သွားပြီ ဒါဆို နောက်တခေါက်ပြန်ကြည့်ဖို့အောက်က ခလုတ်လေးတွေကိုနှိပ်ပြီးရှာကြည့်ပါအုန်း "
        self.no_shops_found = "🤔🤔🤔🤔တောင်းပန်ပါတယ်ခင်ဗျာ မိတ်ဆွေနေတဲ့ နေရာတဝိုက်မှာ ရှိတဲ့ ဆိုင်ကို မတွေ့လို့ပါ။နောက်တခေါက်ပြန်ကြည့်ဖို့ အောက်က ခလုတ်လေးတွေကိုနှိပ်ပြီးရှာကြည့်ပါအုန်း"

    def handle_initial_location_reply(self):
        self.current_user["current_shop_page"] = 1
        self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
        shops = self._query_location_based_shops(self.page_num, self.page_size)
        if len(shops) is not 0:
            self.bot.send_generic_reply(self.sender_id, self._generate_shops(shops, self.is_zawgyi), self.is_zawgyi)
        else:
            self.bot.send_quick_reply(self.sender_id, self.no_shops_found,
                                      self._after_shop_selection_exit(self.is_zawgyi),
                                      self.is_zawgyi)

    def handle_location_base_reply(self, payload):
        if payload == self.NEXT_LOCATION_SHOPS:
            self.page_num = int(self.current_user.get('current_shop_page')) + 1

            shops = self._query_location_based_shops(self.page_num, self.page_size)
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

    def _query_location_based_shops(self, page_num, page_size):
        query = "SELECT * FROM ( SELECT " \
                "id, name_uni, address, lat, lon, (" \
                "3959 * acos ( cos ( radians({0}) ) * cos( radians( lat ) ) * cos( radians( lon ) - radians({1}) )" \
                "+ sin ( radians({2}) ) * sin( radians( lat ) ) )" \
                ") AS distance FROM public.shop )sub".format(decimal.Decimal(self.latitude),
                                                             decimal.Decimal(self.longitude),
                                                             decimal.Decimal(self.latitude))
        print(query)
        where_condition = " WHERE distance<={0}".format(3)
        order_by = " ORDER BY distance ASC "
        return self.shop.query_select(query, where_condition, order_by, int(page_num), int(page_size))

    def _after_shop_selection_exit(self, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဆိုင်တွေကိုကြည့်မယ်") if is_zawgyi else "ဆိုင်တွေကိုကြည့်မယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_fork_knife.png",
                "payload": self.BROWSE_SHOPS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("အနီးနားမှာရှာမယ်") if is_zawgyi else "အနီးနားမှာရှာမယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_location.png",
                "payload": self.SELECT_LOCATION_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ကျွန်တော်တို့အကြောင်း") if is_zawgyi else "ကျွန်တော်တို့အကြောင်း",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_info.png",
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
                "url": "https://ramadan-bazzar-web.web.app/shop/{0}".format(shop.get("id")),
                "webview_height_ratio": "compact",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": "https://ramadan-bazzar-web.web.app/shop/{0}".format(shop.get("id")),
                    "title": Rabbit.uni2zg("Menu ကြည့်မယ်") if is_zawgyi else "Menu ကြည့်မယ်",

                },
                {
                    "type": "postback",
                    "title": Rabbit.uni2zg(
                        "အနီးကဆိုင်တွေကြည့်မယ်") if is_zawgyi else "အနီးကဆိုင်တွေကြည့်မယ်",
                    "payload": self.NEXT_LOCATION_SHOPS
                },
                {
                    "type": "postback",
                    "title": Rabbit.uni2zg("မကြည့်တော့ဘူး") if is_zawgyi else "မကြည့်တော့ဘူး",
                    "payload": self.EXIT_SHOPS
                }
            ]
        } for shop in shops]


class FontSelectionUseCase:

    def __init__(self, sender_id, user, current_user, bot, page_id, recipient_id):
        self.sender_id = sender_id
        self.bot = bot
        self.user = user
        self.current_user = current_user

        self.page_id = page_id
        self.page_recipient_id = recipient_id

        self.is_zawgyi = current_user.get('iszawgyi')
        self.FONT_SELECTION_PAYLOAD = "FONT_SELECTION_PAYLOAD"
        self.ZAW_GYI_PAYLOAD = "ZAW_GYI_PAYLOAD"
        self.UNICODE_PAYLOAD = "UNICODE_PAYLOAD"
        self.current_user = current_user
        self.SELECT_LOCATION_PAYLOAD = "SELECT_LOCATION_PAYLOAD"
        self.BROWSE_SHOPS = "BROWSE_SHOPS"
        self.AVAILABLE_MENUS = "AVAILABLE_MENUS"
        self.ABOUT_US_PAYLOAD = "ABOUT_US_PAYLOAD"
        self.NO_LOCATION_PAYLOAD = "NO_LOCATION_PAYLOAD"

        self.quick_reply_payload = ''
        self.EVENT_FONT_CHANGE = "အောက်မှာ မြင်ရတဲ့ စာသားလေးကိုနှိပ်ပြီး Font ရွေးပေးပါခင်ဗျာ။"
        self.after_font_selection = "ကောင်းပါပြီ ဒါဆို အောက်က menuလေးတွေကို နှိပ်ပြီးကြည့်လို့ရပါပြီခင်ဗျာ။"
        self.no_location_response = "ဟုတ်ပြီ ဒါဆိုရင် တော့ ဒီတိုင်းပဲရှာဖို့ အောက်က ခလုပ်လေးတွေကိုနှိပ်လိုက်ပါခင်ဗျာ။"


    def send_font_selection(self):
        is_zawgyi = False
        self.bot.send_quick_reply(self.sender_id, self.EVENT_FONT_CHANGE, self._font_selection_payload(), is_zawgyi)

    def handle_user_font_selection(self, payload):
        self.quick_reply_payload = payload
        if self.quick_reply_payload == self.FONT_SELECTION_PAYLOAD:
            self.bot.send_quick_reply(self.sender_id, self.EVENT_FONT_CHANGE, self._font_selection_payload(),
                                      self.is_zawgyi)



        if self.quick_reply_payload == self.ZAW_GYI_PAYLOAD:
            self.current_user["iszawgyi"] = True
            self.is_zawgyi = True
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            self.bot.send_quick_reply(self.sender_id, self.after_font_selection,
                                      self._after_font_selection_payload(self.is_zawgyi),
                                      self.is_zawgyi)

        if self.quick_reply_payload == self.UNICODE_PAYLOAD:
            self.current_user["iszawgyi"] = False
            self.is_zawgyi = False
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            self.bot.send_quick_reply(self.sender_id, self.after_font_selection,
                                      self._after_font_selection_payload(self.is_zawgyi),
                                      self.is_zawgyi)

        if self.quick_reply_payload == self.SELECT_LOCATION_PAYLOAD:
            self.bot.send_location_reply(self.sender_id,
                                         "အနီးမှာရှိတဲ့ဆိုင်တွေရှာဖို့ Location access ပေးဖို့လို့ပါတယ်။အကယ်လို့ Location ကိုတောင်းတဲ့ စာလေးပေါ်လာရင် Allow ကိုနှိပ်လိုက်ပါ။",
                                         self.is_zawgyi, self.page_id, self.page_recipient_id)

        if self.quick_reply_payload == self.NO_LOCATION_PAYLOAD:
            self.bot.send_quick_reply(self.sender_id, self.no_location_response,
                                      self._after_font_selection_payload(self.is_zawgyi),
                                      self.is_zawgyi)

    def _after_font_selection_payload(self, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဆိုင်တွေကိုကြည့်မယ််") if is_zawgyi else "ဆိုင်တွေကိုကြည့်မယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_fork_knife.png",
                "payload": self.BROWSE_SHOPS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("အနီးနားမှာရှာမယ်") if is_zawgyi else "အနီးနားမှာရှာမယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_location.png",
                "payload": self.SELECT_LOCATION_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ကျွန်တော်တို့အကြောင်း") if is_zawgyi else "ကျွန်တော်တို့အကြောင်း",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_info.png",
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

        self.is_zawgyi = current_user.get('iszawgyi')
        self.SELECT_LOCATION_PAYLOAD = "SELECT_LOCATION_PAYLOAD"
        self.BROWSE_SHOPS = "BROWSE_SHOPS"
        self.NEXT_SHOPS = "NEXT_SHOPS"
        self.VIEW_SHOP = "VIEW_SHOP"
        self.AVAILABLE_MENUS = "AVAILABLE_MENUS"
        self.ABOUT_US_PAYLOAD = "ABOUT_US_PAYLOAD"
        self.FONT_SELECTION_PAYLOAD = "FONT_SELECTION_PAYLOAD"
        self.EXIT_SHOPS = "EXIT_SHOPS"
        self.after_exit_shops = "ကောင်းပါပြီ ဒါဆို အောက်က သင်ကြည့်လိုတဲ့ လုပ်ဆောင်လိုတဲ့ ခလုတ်လေးတွေကိုနှိပ်လို့ရပါပြီခင်ဗျာ။ "
        self.browse_shops_end = "ဆိုင်တွေအားလုံးကြည့်လိုတော့ကုန်သွားပြီ ဒါဆို နောက်တခေါက်ပြန်ကြည့်ဖို့အောက်က ခလုတ်လေးတွေကိုနှိပ်ပြီးရှာကြည့်ပါအုန်း "
        self.about_us_response="(Assalamualaikum) \n ကိုရိုနာဗိုင်းရစ် ကိုဗစ်-၁၉ ကူးစက်မှုများ ကြောင့်နှစ်စဥ် ရမဇန်ဥပုဒ် ကာလတွင်း ဝါဖြေပွဲ ရောင်းချသူမိတ်ဆွေများ ရောင်းချရန် အတွက် သက်ဆိုင်ရာမှကန့်သတ်မှုများရှိလာနိုင်တဲ့အတွက် ကျတော်တို့ Ramadan Bazaar Myanmar Page ပာာ ရောင်းသူ ဝယ်သူ ချိတ်ဆက် နိုင် အောင် လုပ်ပေးနိုင်သည့်နေရာ တစ်ခုဖြစ်ပါသည်။ ကျတော်တို့တတ်ကျွမ်းသော နည်းပညာကို ဓမ္မဒါန အဖြစ် အစ္စလာမ်ဘာသာဝင်များ အဆင်ပြေစေရန်ကူညီဆောင်ရွက်ခြင်းသာဖြစ်ပါတယ်ဗျာ။"

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

            self.page_num = int(self.current_user.get('current_shop_page')) + 1

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
        if payload == self.ABOUT_US_PAYLOAD:
            self.bot.send_quick_reply(self.sender_id, self.about_us_response,
                                      self._after_font_selection_payload(self.is_zawgyi),
                                      self.is_zawgyi)
        if payload == self.EXIT_SHOPS:
            self.current_user["current_shop_page"] = 1
            self.user.update(self.current_user, "sender_id = {0}".format(self.sender_id))
            self.bot.send_quick_reply(self.sender_id, self.after_exit_shops,
                                      self._after_shop_selection_exit(self.is_zawgyi),
                                      self.is_zawgyi)

    def _after_font_selection_payload(self, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဆိုင်တွေကိုကြည့်မယ််") if is_zawgyi else "ဆိုင်တွေကိုကြည့်မယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_fork_knife.png",
                "payload": self.BROWSE_SHOPS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("အနီးနားမှာရှာမယ်") if is_zawgyi else "အနီးနားမှာရှာမယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_location.png",
                "payload": self.SELECT_LOCATION_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ကျွန်တော်တို့အကြောင်း") if is_zawgyi else "ကျွန်တော်တို့အကြောင်း",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_info.png",
                "payload": self.ABOUT_US_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဖောင့်ပြန်ရွေးရန်") if is_zawgyi else "ဖောင့်ပြန်ရွေးရန်",
                "image_url": "https://raw.githubusercontent.com/winhtaikaung/mm-exchange-rate-check-bot/master/icon_image/ic_unicode.png",
                "payload": self.FONT_SELECTION_PAYLOAD
            }

        ]


    def _after_shop_selection_exit(self, is_zawgyi):
        is_zawgyi = str2bool(is_zawgyi)
        return [
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ဆိုင်တွေကိုကြည့်မယ်") if is_zawgyi else "ဆိုင်တွေကိုကြည့်မယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_fork_knife.png",
                "payload": self.BROWSE_SHOPS
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("အနီးနားမှာရှာမယ်") if is_zawgyi else "အနီးနားမှာရှာမယ်",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_location.png",
                "payload": self.SELECT_LOCATION_PAYLOAD
            },
            {
                "content_type": "text",
                "title": Rabbit.uni2zg("ကျွန်တော်တို့အကြောင်း") if is_zawgyi else "ကျွန်တော်တို့အကြောင်း",
                "image_url": "https://raw.githubusercontent.com/r-phyan-kwee-tech/ramadan-bazaar-mm/master/icons/ic_info.png",
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
                "url": "https://ramadan-bazzar-web.web.app/shop/{0}".format(shop.get("id")),
                "webview_height_ratio": "compact",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": "https://ramadan-bazzar-web.web.app/shop/{0}".format(shop.get("id")),
                    "title": Rabbit.uni2zg("Menu ကြည့်မယ်") if is_zawgyi else "Menu ကြည့်မယ်",

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
