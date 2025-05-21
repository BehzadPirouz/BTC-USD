import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
df = yf.download("BTC-USD", start= "2020-01-01", end= "2024-12-31")
df["Date"] = df.index
df["weekday"] = df["Date"].dt.weekday
df["weekday_name"] = df["Date"].dt.day_name()
wednesdays = df[df["weekday"] == 2].copy()
fridays = df[df["weekday"] == 4].copy()
#print(df[["Open", "Close", "weekday", "weekday_name"]])
#print(wednesdays[["Open", "Close", "weekday"]])
buy_prices = wednesdays[["Date", "Open"]].reset_index(drop= True)
sell_prices = fridays[["Date", "Close"]].reset_index(drop= True)
min_len = min(len(buy_prices), len(sell_prices))
buy_prices = buy_prices.iloc[:min_len]
sell_prices = sell_prices.iloc[:min_len]

capital = 1000
history = [capital]
for i in range(min_len):
    buy_price = buy_prices.loc[i, "Open"].values[0]
    sell_price = sell_prices.loc[i, "Close"].values[0]
    btc_amount = capital / buy_price
    capital = btc_amount * sell_price
    history.append(capital)
print(f"Final Capital after weekly trading: ${capital: .2f}")

plt.figure(figsize=(10, 5))
# print(type(history))
# print(history[:5])
# input("wait")
plt.plot(history, color="darkgreen")
plt.title("Bitcoin Weekly Trading Profit (2020 - 2024)", fontsize=14)
plt.xlabel("Week Number")
plt.ylabel("Capital (USD)")
plt.grid(True)
plt.tight_layout()
plt.savefig("bitcoin_profit.png", dpi=300, bbox_inches="tight")
plt.show()






