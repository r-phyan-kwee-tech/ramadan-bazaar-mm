import gspread
from oauth2client.service_account import ServiceAccountCredentials


def split_pipe_last(input):
    if "|" in input:
        return str(str(input).strip().split("|")[1]).strip()
    else:
        return input


def split_pipe_first(input):
    if "|" in input:
        return str(str(input).strip().split("|")[0]).strip()
    else:
        return input


def replace_empty_images(input):
    if str(input).isspace() == True:
        return "https://via.placeholder.com/840x480/ffffff/ff5252?text={0}".format("no%20image%20available")
    else:
        return input


def importer_mapper(title):
    map = {
        "Shop": shop_data_importer,
        "Menu_Items": menu_item_data_importer,
        "Menu": menu_data_importer,
        "Category": category_data_importer,
        "Region": region_data_importer,
        "Township": township_data_importer,
    }
    return map.get(title)


def shop_data_importer(worksheet):
    print("---SHOP--DATA---")
    print("DELETE FROM shop;")
    print("ALTER SEQUENCE shop_id_seq RESTART WITH 1;")
    cols = ["name_uni", "description", "menu_id", "lat", "lon", "address", "phone_number_1", "phone_number_2",
            "phone_number_3", "township_id", "region_id", "delivery_include"]
    seperator = ","
    col_query = seperator.join(cols)

    for i, item in enumerate(zip(*[worksheet.col_values(col + 1) for col in range(12)])):
        if i > 0:
            result = map(split_pipe_last, item)
            item = dict(zip(cols, list(result)))

            query = "INSERT into shop ({0}".format(col_query)
            query += ") VALUES ('{0}','{1}',{2},{3},{4},'{5}','{6}','{7}','{8}',{9},{10},'{11}');".format(
                *[item.get(field) for field in cols])
            print(query)
    pass


def menu_item_data_importer(worksheet):
    print("---MENU--ITEM--DATA---")
    print("DELETE FROM menu_item;")
    print("ALTER SEQUENCE menu_item_id_seq RESTART WITH 1;")
    cols = ["name_uni", "description_uni", "unit_price", "menu_category_id", "menu_id", "image_url"]
    seperator = ","
    col_query = seperator.join(cols)
    for i, item in enumerate(zip(*[worksheet.col_values(col + 1) for col in range(6)])):
        if i > 0:
            result = map(split_pipe_last, item)
            result = map(replace_empty_images, list(result))
            item = dict(zip(cols, list(result)))

            query = "INSERT into menu_item ({0}".format(col_query)
            query += ") VALUES ('{0}','{1}',{2},{3},{4},'{5}');".format(*[item.get(field) for field in cols])
            print(query)
    pass


def menu_data_importer(worksheet):
    print("---MENU--DATA---")
    print("DELETE FROM menu;")
    print("ALTER SEQUENCE menu_id_seq RESTART WITH 1;")
    cols = ["id", "name_uni"]
    seperator = ","
    col_query = seperator.join(cols)
    for i, item in enumerate(zip(*[worksheet.col_values(col + 1) for col in range(2)])):
        if i > 0:
            result = map(split_pipe_first, item)

            item = dict(zip(cols, list(result)))
            query = "INSERT into menu ({0}".format(col_query)
            query += ") VALUES ({0},'{1}');".format(*[item.get(field) for field in cols])
            print(query)
    pass


def category_data_importer(worksheet):
    print("---MENU--CATEGORY--DATA---")
    print("DELETE FROM menu_category;")
    print("ALTER SEQUENCE menu_category_id_seq RESTART WITH 1;")
    cols = ["id", "name_uni"]
    seperator = ","
    col_query = seperator.join(cols)

    for i, item in enumerate(zip(*[worksheet.col_values(col + 1) for col in range(2)])):
        if i > 0:
            result = map(split_pipe_first, item)
            item = dict(zip(cols, list(result)))
            query = "INSERT into menu_category ({0}".format(col_query)
            query += ") VALUES ({0},'{1}');".format(*[item.get(field) for field in cols])
            print(query)
    pass


def region_data_importer(worksheet):
    print("---REGION--CATEGORY--DATA---")
    print("DELETE FROM region;")
    print("ALTER SEQUENCE region_id_seq RESTART WITH 1;")
    cols = ["id", "name_uni"]

    seperator = ","
    col_query = seperator.join(cols)
    for i, item in enumerate(zip(*[worksheet.col_values(col + 1) for col in range(2)])):
        if i > 0:
            result = map(split_pipe_first, item)
            item = dict(zip(cols, list(result)))
            query = "INSERT into region ({0}".format(col_query)
            query += ") VALUES ({0},'{1}');".format(*[item.get(field) for field in cols])
            print(query)
    pass


def township_data_importer(worksheet):
    print("---TOWNSHIP--CATEGORY--DATA---")
    print("DELETE FROM township;")
    print("ALTER SEQUENCE township_id_seq RESTART WITH 1;")
    cols = ["id", "name_uni","region_id"]

    seperator = ","
    col_query = seperator.join(cols)
    for i, item in enumerate(zip(*[worksheet.col_values(col + 1) for col in range(3)])):
        if i > 0:
            result = map(split_pipe_last, item)
            item = dict(zip(cols, list(result)))
            query = "INSERT into township ({0}".format(col_query)
            query += ") VALUES ({0},'{1}',{2});".format(*[item.get(field) for field in cols])
            print(query)
    pass


def fetch():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client-secret.json', scope)
    sh = gspread.authorize(credentials).open('Ramadan_Bazaar_Myanmar_Vendors_List')

    for ws_count, worksheet in enumerate(sh.worksheets()):
        importer_mapper(worksheet.title)(worksheet)


def main():
    fetch()


if __name__ == "__main__":
    main()
