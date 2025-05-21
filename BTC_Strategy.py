import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
df = yf.download("BTC-USD", start= "2020-01-01", end= "2024-12-31")
df["Date"] = df.index
df["weekday"] = df["Date"].dt.weekday
df["weekday_name"] = df["Date"].dt.day_name()

best_profit = 0
best_buy_day = None
best_sell_day = None
for buy_day in range(7):
    for sell_day in range(buy_day, 7):
        temp_df = df[(df["weekday"] == buy_day) | (df["weekday"] == sell_day)].copy()
        buy_prices = temp_df[temp_df["weekday"] == buy_day].reset_index(drop=True)
        sell_prices = temp_df[temp_df["weekday"] == sell_day].reset_index(drop=True)
        min_len = min(len(buy_prices), len(sell_prices))
        capital = 1000
        history = [capital]
        for i in range(min_len):
            buy = buy_prices.loc[i, "Open"].values[0]
            sell = sell_prices.loc[i, "Close"].values[0]
            capital *= sell / buy
        if capital > best_profit:
            best_profit = capital
            best_buy_day = buy_day
            best_sell_day = sell_day
print(f"Best Strategy:\nBuy On: {best_buy_day}\nSell On: {best_sell_day}\nFinal Capital: {best_profit:.2f}")
best_buy = df[df["weekday"] == best_buy_day].reset_index(drop= True)
best_sell = df[df["weekday"] == best_sell_day].reset_index(drop= True)
min_len = min(len(best_buy), len(best_sell))
best_buy = best_buy.iloc[:min_len]
best_sell = best_sell.iloc[:min_len]
capital = 1000
history = [capital]
for i in range(min_len):
    buy_price = best_buy.loc[i, "Open"].values[0]
    sell_price = best_sell.loc[i, "Close"].values[0]
    btc = capital / buy_price
    capital = btc * sell_price
    history.append(capital)

plt.figure(figsize=(10, 5))
plt.plot(history, color="darkgreen")
plt.title("Bitcoin Weekly Trading Profit (2020 - 2024)", fontsize=14)
plt.xlabel("Week Number")
plt.ylabel("Capital (USD)")
plt.grid(True)
plt.tight_layout()
plt.savefig("bitcoin_strategy.png", dpi=300, bbox_inches="tight")
plt.show()
