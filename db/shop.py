import os


class Shop:
    def __init__(self, db):
        super().__init__()

        # Initialising db connection
        self.db = db
        self.cols=("name","description","menu_id","lat","lon","address","phone_number_1","phone_number_2","phone_number_3","township_id","region_id","delivery_include")

    def insert(self, entity):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO public.shop (name,description,menu_id,lat,lon,address,phone_number_1,phone_number_2,phone_number_3,township_id,region_id,delivery_include) "
            + "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (entity.get(col) for col in self.cols)
        )
        self.db.commit()

    def update(self, entity, condition):
        cursor = self.db.cursor()
        try:
            cursor.execute(
                "UPDATE shop SET sender_id = ?, shop_id= ? ,menu_id= ?,contact_number= ?,address= ? ,quantity= ?, amount= ? , order_status = ? ,isZawgyi=?"
                + "WHERE ?",
                (entity.get("sender_id"), entity.get("shop_id"), entity.get("menu_id"), entity.get("contact_number"),
                 entity.get("address"), entity.get("quantity"),
                 entity.get("amount"), entity.get("order_status"), entity.get("isZawgyi"), condition)
            )

            self.db.commit()

        except Exception as e:
            cursor.close()
            print(e)

    def select(self, condition, page_num, page_size):
        cursor = self.db.cursor()
        select_query = "SELECT * FROM shop "
        try:
            if condition is not None:
                select_query += condition
            # Order by and pagination
            limit = page_size
            offset = (int(page_num) - 1) * page_size

            offset_query = " ORDER BY id ASC LIMIT {0} OFFSET {1} ".format(str(limit), str(offset))
            select_query += offset_query

            if not os.getenv("ENV") == 'production':
                results = cursor.execute(select_query)
            else:
                cursor.execute(select_query)
                results = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            shops = []
            if not os.getenv("ENV") == 'production':
                for row in results:
                    fields = field_names
                    shop = {
                        field: row[field] for field in fields
                    }
                    shops.append(shop)
                return shops
            else:
                for row in results:
                    fields = field_names
                    shop = {
                        field: str(row[x]) for x, field in enumerate(fields)
                    }
                    shops.append(shop)
                return shops
        except Exception as e:
            print("Shop Select", e)
            cursor.close()

            return []

    def query_select(self, query, condition, ordered_by, page_num, page_size):
        cursor = self.db.cursor()

        select_query = query
        try:
            if condition is not None:
                select_query += condition
            # Order by and pagination
            limit = page_size
            offset = (page_num - 1) * page_size
            if ordered_by is not None:
                select_query += ordered_by
            offset_query = " LIMIT {0} OFFSET {1} ".format(limit, offset)
            select_query += offset_query

            if not os.getenv("ENV") == 'production':
                results = cursor.execute(select_query)
            else:
                cursor.execute(select_query)
                results = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            shops = []
            if not os.getenv("ENV") == 'production':
                for row in results:
                    fields = field_names
                    shop = {
                        field: row[field] for field in fields
                    }
                    shops.append(shop)
                return shops
            else:
                for row in results:
                    fields = field_names
                    shop = {
                        field: str(row[x]) for x, field in enumerate(fields)
                    }
                    shops.append(shop)
                return shops
        except Exception as e:
            print(e)

            return []
