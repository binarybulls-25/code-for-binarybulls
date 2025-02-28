import numpy as np


def RSI(prices: np.ndarray, time_period: int = 14) -> np.ndarray:
    if len(prices) <= 1:
        return np.full_like(prices, np.nan)  # Not enough data

    rsi = np.full(len(prices), np.nan)

    alpha = 1 / time_period

    ema_gain = 0
    ema_loss = 0

    prev_price = prices[0]

    for i in range(1, len(prices)):
        current_price = prices[i]
        price_change = current_price - prev_price

        gain = max(price_change, 0)
        loss = max(-price_change, 0)

        ema_gain = alpha * gain + (1 - alpha) * ema_gain
        ema_loss = alpha * loss + (1 - alpha) * ema_loss

        if ema_loss == 0:  # Full bullish market, Handle Divide by 0
            rsi[i] = 100
        else:
            rs = ema_gain / ema_loss
            rsi[i] = round(100 - (100 / (1 + rs)), 2)

        prev_price = current_price

    return rsi
