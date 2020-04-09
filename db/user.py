import os


class User:
    def __init__(self, db):
        super().__init__()

        # Initialising db connection
        self.db = db

    def insert(self, entity):
        cursor = self.db.cursor()
        insert_query = "INSERT INTO public.user (sender_id, shop_id, menu_id, contact_number, address, quantity, amount, order_status) VALUES ({0},{1},{2},'{3}','{4}','{5}','{6}','{7}');".format(
            entity.get('sender_id'), 0, 0, '', '', 0, 0, '')
        print(insert_query)
        try:
            cursor.execute(
                insert_query
            )

            self.db.commit()
        except Exception as e:
            cursor.close()
            print(e)

    def update(self, entity, condition):
        cursor = self.db.cursor()
        update_query = "UPDATE public.user SET sender_id = '{0}', shop_id= '{1}' ,menu_id= '{2}',contact_number= '{3}',address= '{4}' " \
                       ",quantity= '{5}', amount= '{6}' , order_status = '{7}' ,iszawgyi='{8}' , current_shop_page = '{9}' , " \
                       "current_menu_page = '{10}' ".format(
            entity.get("sender_id"), entity.get("shop_id"), entity.get("menu_id"), entity.get("contact_number"),
            entity.get("address"), entity.get("quantity"),
            entity.get("amount"), entity.get("order_status"), entity.get("iszawgyi"),
            entity.get('current_shop_page'), entity.get('current_menu_page'))

        update_query += "WHERE {0}".format(condition)
        try:
            cursor.execute(
                update_query
            )

            self.db.commit()

        except Exception as e:
            cursor.close()
            print("USER Update", e)

    def select(self, condition):
        cursor = self.db.cursor()
        select_query = "SELECT * FROM public.user "
        try:
            if condition is not None:
                select_query += condition

            if not os.getenv("ENV") == 'production':
                results = cursor.execute(select_query)
            else:
                cursor.execute(select_query)
                results = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            users = []
            if not os.getenv("ENV") == 'production':
                for row in results:
                    fields = field_names
                    user = {
                        field: row[field] for field in fields
                    }
                    users.append(user)
                return users
            else:
                for row in results:
                    fields = field_names
                    user = {
                        field: str(row[x]) for x, field in enumerate(fields)
                    }
                    users.append(user)
                return users
        except Exception as e:
            print(e)

            return []


