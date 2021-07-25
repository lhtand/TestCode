import pyupbit as up
import time
import datetime

class WrapBit:
    def __init__(self, access, secret):
        self.upbit = up.Upbit(access, secret)
        print('Set upbit information.')

    def ShowBalance(self, ticker):
        print(ticker, self.upbit.get_balance(ticker))

    def GetTargetPrice(self, ticker, k):
        df = up.get_ohlcv(ticker, interval='day', count=2)
        target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low'])*k
        return target_price

    def GetCurrentPrice(self, ticker):
        return up.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

    def GetStartTime(self, ticker):
        df = up.get_ohlcv(ticker, interval='day', count=1)
        start_time = df.index[0]
        return start_time

    def GetBalance(self, ticker):
        balances = self.upbit.get_balances()
        for b in balances:
          if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
        return 0

    def BuyMarketOrder(self, ticker, percent):
        krw = self.GetBalance('KRW')
        if krw > 5000:
            self.upbit.buy_market_order(ticker, krw * 0.9995 * percent / 100.0)
            print('Buy Coin !')

    def SellMarketOrder(self, ticker, percent):
        coin = self.GetBalance(ticker)
        current_price_coin = self.GetCurrentPrice(ticker)
        if coin > (5000/current_price_coin):
            self.upbit.sell_market_order(ticker, coin*0.9995 * percent / 100.0)
            print('Sell Coin !')

class Algorithm(WrapBit):
    def AutoLarry(self, buy_ticker, sell_ticker, k):
        while True:
            try:
                now = datetime.datetime.now()
                start_time = self.GetStartTime(buy_ticker[0])
                # end_time = start_time + datetime.timedelta(minutes=75)
                end_time = start_time + datetime.timedelta(days=1)

                if start_time < now < end_time - datetime.timedelta(seconds=60):
                    for ticker in buy_ticker:
                        target_price = self.GetTargetPrice(ticker, k)
                        current_price = self.GetCurrentPrice(ticker)
                        if target_price < current_price:
                            self.BuyMarketOrder(buy_ticker, 100)
                else:
                    for ticker in sell_ticker:
                        self.SellMarketOrder(sell_ticker, 100)

                time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)