from download_data import download_historical_data
import pandas as pd
import os
from backtesting import Backtest

from rsi_simpleStrategy import RSISimpleStrategy


def prepare_ticks_data_backtesting(
    df: pd.DataFrame, time_column_name: str = "datetime"
):
    df = df.rename(
        columns={time_column_name: "Date"}
    )  # Backtesting.py Expects Date for timestamp index
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by="Date")
    df = df[["Date", "open", "high", "low", "close", "volume"]]
    df.set_index("Date", inplace=True)
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    return df


def run_rsisimple(df, params, plot_result=False):
    initial_cash = 1_000_000

    bt = Backtest(
        df, RSISimpleStrategy, cash=initial_cash, commission=0, exclusive_orders=True
    )

    stats = bt.run(
        rsi_period=14,
        oversold=params["oversold"],
        overbought=params["overbought"],
        stop_loss=params["stop_loss"],
        take_profit=params["take_profit"],
    )

    results = {
        "Risk to Reward": "1:2",
        "# of Trades": stats["# Trades"],
        "Win%": stats["Win Rate [%]"],
        "Final P&L": stats["Equity Final [$]"] - initial_cash,
        "ROI": ((stats["Win Rate [%]"] / 100 * 2) - (1 - (stats["Win Rate [%]"] / 100)))
        * 100,
    }

    if plot_result:
        bt.plot(plot_volume=False)

    return results


def main():
    filepath_5mins = "data/ESH5_5mins_data.csv"
    params = {"oversold": 30, "overbought": 70, "stop_loss": 10, "take_profit": 20}

    if os.path.exists(filepath_5mins):
        df_5mins = pd.read_csv(filepath_5mins)
    else:
        df_5mins = download_historical_data(durationStr="1 Y", bar_size="5 mins")
        df_5mins.to_csv(filepath_5mins)

    df_5mins = prepare_ticks_data_backtesting(df_5mins)

    # filepath_3mins = "data/ESH5_3mins_data.csv"
    # if os.path.exists(filepath_3mins):
    #     pd.read_csv(filepath_3mins)
    # else:
    #     df_3mins = download_historical_data(durationStr="1 Y", bar_size="3 mins")
    #     df_3mins.to_csv("data/ESH5_3mins_data.csv")

    # df_3mins = prepare_ticks_data_backtesting(df_3mins)

    simple_results = run_rsisimple(df_5mins, params)  # Test 5 mins
    # simple_results = run_rsisimple(df_3mins) # Test 3 mins

    # # simple_results = run_rsisimple(df_5mins, params)

    print("Simple RSI Results:", simple_results)


if __name__ == "__main__":
    main()
