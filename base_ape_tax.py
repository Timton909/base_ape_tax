import requests, time

def ape_tax():
    print("Base — Ape Tax Detector (tax drops to 0% post-launch)")
    known = {}  # pair → initial tax

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                buy_tax = pair.get("buyTax")
                sell_tax = pair.get("sellTax")
                age = time.time() - pair.get("pairCreatedAt", 0) / 1000

                if age > 600: continue  # older than 10 min

                if addr not in known:
                    if buy_tax is not None and sell_tax is not None:
                        known[addr] = (buy_tax, sell_tax)
                    continue

                old_buy, old_sell = known[addr]
                if (old_buy > 5 or old_sell > 5) and buy_tax == 0 and sell_tax == 0:
                    token = pair["baseToken"]["symbol"]
                    print(f"APE TAX DROPPED TO 0%\n"
                          f"{token} — dev removed tax after launch\n"
                          f"Was: Buy {old_buy}% / Sell {old_sell}%\n"
                          f"Now: 0% / 0%\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Fair launch mode activated — apes incoming\n"
                          f"{'TAX ZERO'*20}")
                    del known[addr]

        except:
            pass
        time.sleep(5.3)

if __name__ == "__main__":
    ape_tax()
