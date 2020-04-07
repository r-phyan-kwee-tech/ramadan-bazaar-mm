class Shop:
    def __init__(self, db):
        super().__init__()

        # Initialising db connection
        self.db = db

    def insert(self, entity):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO 'shop' ('sender_id', 'shop_id', 'menu_id', 'contact_number', 'address', 'quantity', 'amount', 'order_status') "
            + "VALUES (?,?,?,?,?,?,?,?)",
            (entity.get('sender_id'), 0, 0, '', '', '', '', '')
        )
        self.db.commit()

    def update(self, entity, condition):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                "UPDATE shop SET sender_id = ?, shop_id= ? ,menu_id= ?,contact_number= ?,address= ? ,quantity= ?, amount= ? , order_status = ? ,isZawgyi=?"
                + "WHERE ?",
                (entity.get("sender_id"), entity.get("shop_id"), entity.get("menu_id"), entity.get("contact_number"), entity.get("address"), entity.get("quantity"),
                 entity.get("amount"), entity.get("order_status"), entity.get("isZawgyi"),condition)
            )

            self.db.commit()

        except Exception as e:
            print(e)


    def select(self, condition,page_num,page_size):
        cursor = self.db.cursor()
        select_query = "SELECT * FROM shop "
        try:
            if condition is not None:
                select_query += condition
            # Order by and pagination
            limit = page_size
            offset = (page_num - 1) * page_size
            select_query += " ORDER BY id ASC LIMIT ? OFFSET ?"

            args = (limit, offset)

            results=cursor.execute(select_query,args)
            field_names = [i[0] for i in cursor.description]
            shops = []
            for row in results:
                fields = field_names
                shop = {
                    field: row[field] for field in fields
                }
                shops.append(shop)
            return shops
        except Exception as e:
            print(e)

            return []



