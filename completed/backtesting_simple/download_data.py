"""
From Video 1: Make money using algotrading
"""

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time
import pandas as pd

DEFAULT_HOST: str = "127.0.0.1"
DEFAULT_PORT: int = 7497
DEFAULT_CLIENT_ID: int = 0


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = []
        self.event = threading.Event()

    def historicalData(self, reqId, bar):
        self.data.append(
            {
                "datetime": bar.date,
                "open": bar.open,
                "high": bar.high,
                "low": bar.low,
                "close": bar.close,
                "volume": bar.volume,
            }
        )

    def historicalDataEnd(self, reqId, start, end):
        self.event.set()


def download_historical_data(
    symbol: str = "ES",
    contract_date: str = "202503",
    durationStr: str = "2 D",
    bar_size: str = "3 mins",
):
    app = TradeApp()

    def websocket_con():
        app.run()

    app.connect(host=DEFAULT_HOST, port=DEFAULT_PORT, clientId=DEFAULT_CLIENT_ID)

    conn_thread = threading.Thread(target=websocket_con, daemon=True)
    conn_thread.start()

    time.sleep(1)

    contract = Contract()

    contract.symbol = symbol
    contract.secType = "FUT"
    contract.currency = "USD"
    contract.exchange = "CME"
    contract.lastTradeDateOrContractMonth = contract_date

    app.reqHistoricalData(
        reqId=0,
        contract=contract,
        endDateTime="",
        durationStr=durationStr,
        barSizeSetting=bar_size,
        whatToShow="TRADES",
        useRTH=1,
        formatDate=1,
        keepUpToDate=False,
        chartOptions=[],
    )

    app.event.wait()

    app.disconnect()

    df = pd.DataFrame(app.data)
    return df
