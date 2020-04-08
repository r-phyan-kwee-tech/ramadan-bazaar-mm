from db.shop import Shop


class ShopUseCase:
    def __init__(self, shop_id, db):
        self.shop_id = shop_id
        self.db = db
        self.shop = Shop(db)

    def fetch_shop_detail(self):
        query = "SELECT SH.id as shop_id,SH.name_uni,SH.address,SH.phone_number_1,SH.phone_number_2," \
                "SH.phone_number_3, MI.name_uni as menu_item_name,MI.description_uni,MI.unit_price,MC.name_uni as " \
                "menu_category_name from menu_item as MI INNER JOIN menu_category as MC on MI.menu_category_id=MC.id " \
                "INNER JOIN shop as SH on SH.menu_id=MI.menu_id "
        where_condition = " WHERE SH.id={0}".format(self.shop_id)
        return self.shop.query_select(query, where_condition, 1, 100)
