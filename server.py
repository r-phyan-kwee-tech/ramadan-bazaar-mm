import json
import logging
import os
import sqlite3

import psycopg2
import tornado.options
import tornado.web
from dotenv import load_dotenv


class App(tornado.web.Application):

    def __init__(self, handlers, **kwargs):
        super().__init__(handlers, **kwargs)

        # Initialising db connection
        self.load_env()
        self.db = None
        if not os.environ['ENV'] == 'production':
            self.db = sqlite3.connect("bazaar.db")
            self.db.row_factory = sqlite3.Row
            self.init_db()
        else:

            self.db = psycopg2.connect(
                os.getenv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/db_ramadan_bazar"))
            self.init_pg_db()

    def init_db(self):
        cursor = self.db.cursor()

        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS shop ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "description TEXT,"
            + "lat DECIMAL NOT NULL,"
            + "lon DECIMAL NOT NULL,"
            + "menu_id INTEGER NOT NULL,"
            + "address TEXT NOT NULL,"
            + "phone_number_1 TEXT NOT NULL,"
            + "phone_number_2 TEXT NOT NULL,"
            + "phone_number_3 TEXT NOT NULL,"
            + "township_id INTEGER NOT NULL,"
            + "region_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'region' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"

        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'township' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "region_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'menu' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"

        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'menu_item' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "unit_price INTEGER NOT NULL,"
            + "description_uni TEXT NOT NULL,"
            + "description_zawgyi TEXT NOT NULL,"
            + "menu_category_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "menu_id	INTEGER"
            + ");"

        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'menu_category' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"

        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'orders' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "sender_id INTEGER NOT NULL,"
            + "shop_id INTEGER NOT NULL,"
            + "menu_id INTEGER NOT NULL,"
            + "menu_item_id INTEGER NOT NULL,"
            + "quantity INTEGER NOT NULL,"
            + "order_type INTEGER NOT NULL,"
            + "unit_price DECIMAL NOT NULL,"
            + "total_price DECIMAL NOT NULL,"
            + "address TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'user' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "sender_id INTEGER NOT NULL,"
            + "shop_id TEXT NOT NULL,"
            + "menu_id INTEGER ,"
            + "contact_number TEXT NOT NULL,"
            + "current_shop_page number NOT NULL DEFAULT 1,"
            + "current_menu_page number NOT NULL DEFAULT 1,"
            + "address TEXT NOT NULL,"
            + "quantity INTEGER ,"
            + "lat DECIMAL,"
            + "lon DECIMAL,"
            + "amount INTEGER ,"
            + "isZawgyi BOOLEAN,"
            + "order_status TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP "
            + ");"
        )
        self.db.commit()

    def init_pg_db(self):
        cursor = self.db.cursor()

        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS shop ("
            + " ID  SERIAL PRIMARY KEY,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "description TEXT,"
            + "lat DECIMAL NOT NULL,"
            + "lon DECIMAL NOT NULL,"
            + "menu_id INTEGER NOT NULL,"
            + "address TEXT NOT NULL,"
            + "phone_number_1 TEXT NOT NULL,"
            + "phone_number_2 TEXT NOT NULL,"
            + "phone_number_3 TEXT NOT NULL,"
            + "township_id INTEGER NOT NULL,"
            + "region_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS region ("
            + " ID  SERIAL PRIMARY KEY,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"

        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS township ("
            + " ID  SERIAL PRIMARY KEY,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "region_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS menu ("
            + " ID  SERIAL PRIMARY KEY,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"

        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS menu_item ("
            + " ID  SERIAL PRIMARY KEY,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "unit_price INTEGER NOT NULL,"
            + "description_uni TEXT NOT NULL,"
            + "description_zawgyi TEXT NOT NULL,"
            + "menu_category_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "menu_id	INTEGER"
            + ");"

        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS menu_category ("
            + " ID  SERIAL PRIMARY KEY,"
            + "name_uni TEXT NOT NULL,"
            + "name_zawgyi TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"

        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS orders ("
            + "ID  SERIAL PRIMARY KEY,"
            + "sender_id INTEGER NOT NULL,"
            + "shop_id INTEGER NOT NULL,"
            + "menu_id INTEGER NOT NULL,"
            + "menu_item_id INTEGER NOT NULL,"
            + "quantity INTEGER NOT NULL,"
            + "order_type INTEGER NOT NULL,"
            + "unit_price DECIMAL NOT NULL,"
            + "total_price DECIMAL NOT NULL,"
            + "address TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS public.user ( "
            + "ID SERIAL PRIMARY KEY,"
            + "sender_id bigint NOT NULL,"
            + "shop_id TEXT NOT NULL,"
            + "menu_id INTEGER ,"
            + "contact_number TEXT NOT NULL,"
            + "current_shop_page INTEGER NOT NULL DEFAULT 1,"
            + "current_menu_page INTEGER NOT NULL DEFAULT 1,"
            + "address TEXT NOT NULL,"
            + "lat DECIMAL,"
            + "lon DECIMAL,"
            + "quantity INTEGER ,"
            + "amount INTEGER ,"
            + "iszawgyi BOOLEAN,"
            + "order_status TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP "
            + ");"
        )
        self.db.commit()

    def load_env(self):
        load_dotenv()


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):

        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def write_json(self, obj, status_code=200):
        self.set_header("Content-Type", "application/json")
        self.set_status(status_code)
        self.write(json.dumps(obj))


class PingHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write("pong!")


def make_app(options):
    from messenger.handler import MessengerHandler
    from shop.handler import ShopHandler
    return App([
        (r"/app/ping", PingHandler),
        (r"/messenger", MessengerHandler),
        (r'/api/v1/shop/([^/d]*)/$', ShopHandler),
    ], debug=options.debug)


if __name__ == "__main__":
    # Define settings/options for the web app
    # Specify the port number to start the web app on (default value is port 6000)
    tornado.options.define("port", os.getenv('PORT', 3000))
    # Specify whether the app should run in debug mode
    # Debug mode restarts the app automatically on file changes
    tornado.options.define("debug", default=False)

    # Read settings/options from command line
    tornado.options.parse_command_line()

    # Access the settings defined
    options = tornado.options.options

    # Create web app
    app = make_app(options)
    app.listen(options.port)
    logging.info("Starting listing service. PORT: {}, DEBUG: {}".format(
        options.port, options.debug))

    # Start event loop
    tornado.ioloop.IOLoop.instance().start()
