import logging
import decimal
from broker_clients import session
from broker_clients import Balances, Trades

MINIMUM_TRADE_AMOUNT = 0
logger = logging.getLogger(__name__)


class BrokerEmulator:
    def __init__(self, balance_name=None, balance_id=None):
        if balance_name:
            self.balance_name = balance_name
        if balance_id:
            self.balance_id = balance_id

        self.balance = self.get_balance(balance_name, balance_id)

    def get_balance(self, balance_name=None, balance_id=None):
        if balance_name is None and balance_id is None:
            raise ValueError('No balance id or name provided')
        balance = None

        if balance_name:
            balance = session.query(Balances).filter_by(name=balance_name).first()
        if balance is None:
            balance = session.query(Balances).filter_by(balance_id=balance_id).first()
            if balance is None:
                raise ValueError('No Balance found with name: {} or id: {}'.format(balance_name, balance_id))
            else:
                self.balance_name = balance.name
        else:
            self.balance_id = balance.balance_id
        return balance

    def has_open_order(self):
        return self.count_opened_trades() == 1

    def query_open_trades(self):
        return session.query(Trades).filter_by(name=self.balance_name, sell_price=None, profit=None)

    def count_opened_trades(self):
        return self.query_open_trades().count()

    @ property
    def stop_loss(self):
        return self.trade.stop_loss

    @ stop_loss.setter
    def stop_loss(self, value):
        self.trade.stop_loss = value
        session.commit()

    @property
    def trade(self):
        return self.query_open_trades().first()

    @property
    def trade_id(self):
        return self.trade.trade_id

    @property
    def trade_budget(self):
        return self.balance.free

    def market(self, side, amount, stop_loss=None, stop_loss_percentage=None, emulated_time=None):
        if side not in ['BUY', 'SELL'] or amount <= MINIMUM_TRADE_AMOUNT:
            raise ValueError('Invalid side: {} or amount: {} in market order'.format(side, amount))
        if stop_loss is None and stop_loss_percentage is None:
            raise ValueError('Stop loss must be set')
        if self.count_opened_trades() >= 1:
            raise ValueError('There are {} opened trades'.format(side))
        close_price = decimal.Decimal(emulated_time['Close'])
        calculated_stop_loss = None
        if side == 'BUY':
            if not stop_loss:
                calculated_stop_loss = close_price - (close_price * stop_loss_percentage)

            trade = Trades(name=self.balance_name,
                           symbol=self.balance.symbol,
                           time_frame=self.balance.time_frame,
                           entry_date=emulated_time['date'],
                           amount=amount,
                           stop_loss=calculated_stop_loss,
                           buy_price=close_price,
                           sell_price=None,
                           profit=None,
                           side=side,
                           low_moment_price=emulated_time['Low'],
                           balance_id=self.balance_id)
            session.add(trade)
            session.commit()

    def take_profit(self, row=None):
        close_price = decimal.Decimal(row['Close'])
        delta = close_price - self.trade.buy_price
        profit_percentage = delta / close_price
        profit_amount = self.trade.amount * profit_percentage
        self.set_sell_price(close_price, self.trade.amount + profit_amount, row)
        return {
            "profit_percentage": profit_percentage,
            "profit_amount": profit_amount
        }

    def set_sell_price(self, sell_price, profit, row):
        current_trade = self.trade
        current_trade.sell_price = sell_price
        current_trade.profit = self.balance.symbol_metadata.fix_price_precision(profit)
        current_trade.exit_date = row['date']
        self.balance.free = current_trade.profit
        session.commit()


if __name__ == '__main__':
    balance_name = ''
    broker = BrokerEmulator(balance_name)
    side, amount, stop_loss, stop_loss_percentage, emulated_time = 'BUY', 100, 145, None, {
        "Close": 150, "date": "2021/01/14, 14:30:00"}
    broker.market(side, amount, stop_loss=stop_loss, emulated_time=emulated_time)
