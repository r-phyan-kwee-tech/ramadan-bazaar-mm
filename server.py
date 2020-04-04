import tornado.web
import tornado.log
import tornado.options
import sqlite3
import logging
import json
import time


class App(tornado.web.Application):

    def __init__(self, handlers, **kwargs):
        super().__init__(handlers, **kwargs)

        # Initialising db connection
        self.db = sqlite3.connect("bazaar.db")
        self.db.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        cursor = self.db.cursor()

        # Create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'shop' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name INTEGER NOT NULL,"
            + "lat TEXT NOT NULL,"
            + "lon INTEGER NOT NULL,"
            + "menu_id INTEGER NOT NULL,"
            + "address INTEGER NOT NULL,"
            + "township_id INTEGER NOT NULL,"
            + "region_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'region' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL"
            + ");"


        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'township' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name INTEGER NOT NULL,"
            + "region_id INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ,"
            + "updated_at TIMESTAMP NOT NULL"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'menu' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL"
            + ");"

        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'menu_item' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "name INTEGER NOT NULL,"
            + "unit_price INTEGER NOT NULL,"
            + "description INTEGER NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL"
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
            + "updated_at TIMESTAMP NOT NULL"
            + ");"
        )

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS 'sender' ("
            + "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            + "sender_id INTEGER NOT NULL,"
            + "shop_id TEXT NOT NULL,"
            + "menu_id INTEGER NOT NULL,"
            + "menu_item_id INTEGER NOT NULL,"
            + "contact_number TEXT NOT NULL,"
            + "address TEXT NOT NULL,"
            + "quantity INTEGER NOT NULL,"
            + "amount INTEGER NOT NULL,"
            + "order_status TEXT NOT NULL,"
            + "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            + "updated_at TIMESTAMP NOT NULL"
            + ");"
        )

        self.db.commit()


class BaseHandler(tornado.web.RequestHandler):
    def write_json(self, obj, status_code=200):
        self.set_header("Content-Type", "application/json")
        self.set_status(status_code)
        self.write(json.dumps(obj))

# /listings


class MessengerHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):

        self.write_json({"result": True, "listings": []})

    @tornado.gen.coroutine
    def post(self):

        self.write_json({"result": True, "listing": []})

# /listings/ping


class PingHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.write("pong!")


def make_app(options):
    return App([
        (r"/app/ping", PingHandler),
        (r"/app", MessengerHandler),
    ], debug=options.debug)


if __name__ == "__main__":
    # Define settings/options for the web app
    # Specify the port number to start the web app on (default value is port 6000)
    tornado.options.define("port", default=3000)
    # Specify whether the app should run in debug mode
    # Debug mode restarts the app automatically on file changes
    tornado.options.define("debug", default=True)

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
