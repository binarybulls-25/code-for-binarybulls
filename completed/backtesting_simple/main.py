from download_data import download_historical_data
import pandas as pd
import os
from backtesting import Backtest
from rsi_simpleStrategy import RSISimpleStrategy
import warnings
import itertools
from tabulate import tabulate

warnings.simplefilter("ignore")

def prepare_ticks_data_backtesting(df: pd.DataFrame, time_column_name: str = "datetime"):
    df = df.rename(columns={time_column_name: "Date"})  # Backtesting.py Expects Date for timestamp index
    df["Date"] = pd.to_datetime(df["Date"])

    # Filter data for August and beyond(sparse data, not all bars are present)
    df = df[df["Date"] >= "2024-08-01"]


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
    #print(stats)
    if params["take_profit"] / params["stop_loss"] >= 2:
        risk_to_reward = "1:2"
        roi_val = round((((stats["Win Rate [%]"] / 100 * 2) - (1 - (stats["Win Rate [%]"] / 100)))) * 100,2)
    else:
        risk_to_reward = "1:1"
        roi_val = abs(round(stats["Win Rate [%]"], 2))
        
    results = {
        "Timeframe": params["timeframe"],
        "RSI": f"{params['oversold']}/{params['overbought']}",
        "SL/TP": f"{params['stop_loss']}/{params['take_profit']}",
        "Risk:Reward": risk_to_reward,
        "# Trades": stats["# Trades"],
        "Win%": round(stats["Win Rate [%]"], 2),
        "Final P&L": stats["Equity Final [$]"] - initial_cash,
        "ROI%": round(roi_val, 2)
    }
    
    if plot_result:
        bt.plot(plot_volume=False)
    
    return results

def expirement_param():
    # Define all combinations to test
    rsi_thresholds = [
        {"oversold": 30, "overbought": 70},
        {"oversold": 20, "overbought": 80},
        {"oversold": 10, "overbought": 90}
    ]
    
    timeframes = ["5 mins", "3 mins"]
    
    sl_tp_pairs = [
        {"stop_loss": 10, "take_profit": 20},
        {"stop_loss": 10, "take_profit": 10}
    ]
    
    
    all_results = []
    
    # Load or download data
    for timeframe in timeframes:
        filename = f"data/ESH5_{timeframe.replace(' ', '')}_data.csv"
        
        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = download_historical_data(durationStr="1 Y", bar_size=timeframe)
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            df.to_csv(filename)
            
        df = prepare_ticks_data_backtesting(df)
        
        # Run all parameter combinations
        for rsi_threshold in rsi_thresholds:
            for sl_tp in sl_tp_pairs:
                params = {
                    **rsi_threshold,
                    **sl_tp,
                    "timeframe": timeframe
                }
                
                result = run_rsisimple(df, params)
                all_results.append(result)
    
    # Sort results by ROI (best performers first)
    all_results.sort(key=lambda x: x["Final P&L"], reverse=True)
    
    # Display results in a well-formatted table
    headers = ["Timeframe", "RSI", "SL/TP", "Risk:Reward", "# Trades", "Win%", "Final P&L", "ROI%"]
    rows = [[result[h] for h in headers] for result in all_results]
    
    print("\n=== RSI Strategy Backtest Results (Sorted by Final P&L) ===")
    print(tabulate(rows, headers=headers, tablefmt="grid"))
    
    # Also save results to CSV
    results_df = pd.DataFrame(all_results)
    results_df.to_csv("rsi_backtest_results.csv", index=False)
    print("\nResults saved to 'rsi_backtest_results.csv'")
    
    # Print top 3 performing parameter sets
    print("\nTop 3 Performing Parameter Sets:")
    top3_rows = [[result[h] for h in headers] for result in all_results[:3]]
    print(tabulate(top3_rows, headers=headers, tablefmt="grid"))

def main():
    filepath_5mins = "data/ESH5_5mins_data.csv"
    os.makedirs(os.path.dirname(filepath_5mins), exist_ok=True)

    params = {"oversold": 30, "overbought": 70, "stop_loss": 10, "take_profit": 20,"timeframe":"5 mins"}

    if os.path.exists(filepath_5mins):
        df_5mins = pd.read_csv(filepath_5mins)
    else:
        df_5mins = download_historical_data(durationStr="1 Y", bar_size="5 mins")
        df_5mins.to_csv(filepath_5mins)

    df_5mins = prepare_ticks_data_backtesting(df_5mins)

    filepath_3mins = "data/ESH5_3mins_data.csv"
    if os.path.exists(filepath_3mins):
        df_3mins = pd.read_csv(filepath_3mins)
    else:
        df_3mins = download_historical_data(durationStr="1 Y", bar_size="3 mins")
        df_3mins.to_csv("data/ESH5_3mins_data.csv")

    df_3mins = prepare_ticks_data_backtesting(df_3mins)

    simple_results = run_rsisimple(df_5mins, params, plot_result=False)  # Test 5 mins
    #simple_results = run_rsisimple(df_3mins, params) # Test 3 mins

    # # simple_results = run_rsisimple(df_5mins, params)

    print("Simple RSI Results:", simple_results)

    #expirement_param()

if __name__ == "__main__":
    main()