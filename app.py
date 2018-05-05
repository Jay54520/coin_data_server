import datetime
import json
import tornado.ioloop
import tornado.web
from coin_data.factory import make_data_source

coin_market_cap = make_data_source()

global_coin_ids = coin_market_cap.coin_ids()


class CoinIdHandler(tornado.web.RequestHandler):
    def get(self):
        global_coin_ids = coin_market_cap.coin_ids()
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(global_coin_ids))


class HistoricalHandler(tornado.web.RequestHandler):
    DATE_FORMAT = '%Y-%m-%d'

    def get(self, coin_id):
        if coin_id not in global_coin_ids:
            self.set_status(404)
            self.finish("coin_id \"{}\" not exists".format(coin_id))
        start_day = datetime.datetime.strptime(self.get_query_argument('start_day'), self.DATE_FORMAT)
        end_day = datetime.datetime.strptime(self.get_query_argument('end_day'), self.DATE_FORMAT)
        coins = coin_market_cap.historical_data(coin_id, start_day, end_day)
        historical_data = [coin.pre_json_dict() for coin in coins]
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(json.dumps(historical_data))


def make_app():
    return tornado.web.Application([
        (r"/coin_ids", CoinIdHandler),
        (r"/([^/]+)/historical_data", HistoricalHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
