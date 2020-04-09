import tornado

from server import BaseHandler
from shop.usecase import ShopUseCase


class ShopHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self, shop_id):
        shop_uc = ShopUseCase(shop_id, self.application.db)
        menu_items = shop_uc.fetch_shop_detail()
        return self.write_json({"result": True, "menu_items": menu_items})
