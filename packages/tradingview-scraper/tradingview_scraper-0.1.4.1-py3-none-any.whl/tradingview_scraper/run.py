from tradingview_scraper import *

# Functionality test
# obj = Ideas()
# res = obj.scraper(
#         symbol= "btc",
#         startPage = 1,
#         endPage = 2,
#         to_csv = True,
#         return_json = True,
#     )

obj = Indicators()
res = obj.scraper(
    exchange = "BITSTAMP",
        symbols = ["BTCUSD", "LTCUSDT"],
        indicators = ["RSI", "Stoch.K"],
        allIndicators = True
)
print(res)