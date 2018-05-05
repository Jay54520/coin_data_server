import json
import tornado.ioloop
import tornado.web
from coin_data.factory import make_data_source

coin_market_cap = make_data_source()


class CoinIdHandler(tornado.web.RequestHandler):
    def get(self):
        coin_ids = coin_market_cap.coin_ids()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(coin_ids))


class HistoricalHandler(tornado.web.RequestHandler):
    def get(self, symbol):
        pass


def make_app():
    return tornado.web.Application([
        (r"/coin_ids", CoinIdHandler),
        (r"/([^/]+)/historical_data", CoinIdHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
