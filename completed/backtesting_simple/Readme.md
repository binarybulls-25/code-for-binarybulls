# RSI Backtesting

## Data Download Link

[**ES 5 mins Data**](https://drive.google.com/file/d/1UDWB_sMHCfEKkxRUWU0aR-mPsUOZBaGP/view?usp=share_link)

This repository contains a backtesting setup for evaluating a simple RSI-based trading strategy using **Backtesting.py**. The strategy tests different Overbought/Oversold (OB/OS) levels and risk-to-reward ratios to compare performance.

---

## **Testing Parameters**

### **1. Overbought/Oversold (OB/OS) Levels**
- 70/30
- 80/20
- 90/10

### **2. Risk-to-Reward Ratios**
- 1:1
- 1:2

### **3. Performance Metrics Evaluated**
- **Risk to Reward Ratio**
- **Number of Trades Taken**
- **Win Percentage**
- **Final Profit & Loss (P&L)**
- **Return on Investment (ROI)**

---

## **Project Structure**

```
├── data/                   # Directory for storing historical price data (5 mins, 3 mins, 2000T)
├── download_data.py        # Script for downloading historical data
├── indicators.py           # RSI Indicator implementation
├── rsi_simpleStrategy.py   # RSI-based trading strategy
├── main.py                 # Main backtesting script
└── README.md               # Project documentation
```

---

## **Installation & Setup**

<details>
  <summary>🔽 Click to expand setup instructions</summary>

### **1. Clone the Repository**
```sh
git clone https://github.com/binarybulls-25/code-for-binarybulls.git

```

### **2. Create and Activate Virtual Environment**
```sh
# Mac/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```
### **3. Install Dependencies**
Ensure you have Python installed, then install the required libraries:
```sh
pip install -r requirements.txt
```

### **4. Set Environment Variables**
```sh
# Mac/Linux
export PYTHONPATH=$PYTHONPATH:$PWD

# Windows (PowerShell)
$env:PYTHONPATH = "$env:PYTHONPATH;$PWD"
```




</details>

---

## **Run Backtest**
```sh
cd completed/backtesting_simple
python main.py
```

---

## **Backtesting Workflow**
1. **Download Historical Data**: If local data is unavailable, the script fetches 1-year historical price data at a 5-minute interval.
2. **Data Preparation**: Converts raw price data into a format compatible with Backtesting.py.
3. **Strategy Execution**: Runs the RSI-based strategy with predefined OB/OS levels and risk-to-reward settings.
4. **Results Evaluation**: Outputs trade statistics, including win rate, P&L, and ROI.

---

## **Example Output**
```
Simple RSI Results: {
    'Risk to Reward': '1:2',
    '# of Trades': 150,
    'Win%': 58.3,
    'Final P&L': 12500,
    'ROI': 16.6
}
```

---

## **Next Steps**
- Expand the strategy to test different timeframes (e.g., 3 min, 15 min)
- Implement additional Bearish and Bullish Divergence (aiming for higher win%, fewer trades, and greater ROI)
- Optimize risk management parameters

---

## **License**
This project is licensed under the MIT License.

---

## **Contributions**
For any questions or contributions, feel free to open an issue or submit a pull request!

