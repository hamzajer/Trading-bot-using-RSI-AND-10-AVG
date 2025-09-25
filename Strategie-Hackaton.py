# python -m pip install requests

import json
import requests
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
URL = "http://fx-trading-game-ensimag-challenge.westeurope.azurecontainer.io:443/"
TRADER_ID = "#####"


class Side:
    BUY = "buy"
    SELL = "sell"

def get_price_history(product: str):
    url = f"{URL}/priceHistory/{product}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_price():
    api_url = URL + "/price/EURGBP"
    res = requests.get(api_url)
    if res.status_code == 200:
        return json.loads(res.content.decode('utf-8'))["price"]
    return None


def trade(trader_id, qty, side):
    api_url = URL + "/trade/EURGBP"
    data = {"trader_id": trader_id, "quantity": qty, "side": side}
    res = requests.post(api_url, json=data)
    if res.status_code == 200:
        resp_json = json.loads(res.content.decode('utf-8'))
        if resp_json["success"]:
            return resp_json["price"]
    return None

#
print("Expected to trade at:" + str(get_price()))
print("Effectively traded at:" ,trade(TRADER_ID, 100, Side.BUY))
#

stop_loss= 0.836
take_profit = 0.932
EURGBP= list(get_price_history("EURGBP").values())
# prices = np.array(EURUSD)
# relevant_prices = EURGBP[:-14]
# stop_loss_index = np.where[relevant_prices < stop_loss][0]
# take_profit_index = np.where[relevant_prices < take_profit][0]

def compute_rsi(prices, period: int = 14):
    """Compute RSI from a list of prices."""
    df = pd.DataFrame(prices, columns=["price"])
    df["delta"] = df["price"].diff()

    df["gain"] = df["delta"].clip(lower=0)
    df["loss"] = -df["delta"].clip(upper=0)

    # Wilder’s moving average
    df["avg_gain"] = df["gain"].rolling(window=period, min_periods=period).mean()
    df["avg_loss"] = df["loss"].rolling(window=period, min_periods=period).mean()

    # RS and RSI
    df["rs"] = df["avg_gain"] / df["avg_loss"]
    df["rsi"] = 100 - (100 / (1 + df["rs"]))

    return df["rsi"].iloc[-1]
period = 14

# Calculer le RSI sur les derniers 'period' prix
rsi_now = compute_rsi(EURGBP[-period:], period=period)
print("RSI actuel :", rsi_now)
print(rsi_now)
state = True
def moving_average(prices, window=10):
    """
    Calcule la moyenne mobile simple sur 'window' dernières valeurs.
    """
    if len(prices) < window:
        return None  # Pas assez de données
    return sum(prices[-window:]) / window

def is_ma_increasing(prices, window=10):
    """
    Retourne True si la moyenne mobile est croissante (comparaison avec la précédente).
    """
    if len(prices) < window + 1:
        return None  # Pas assez de données pour comparer
    ma_current = moving_average(prices[-window:])
    ma_previous = moving_average(prices[-window-1:-1])
    return ma_current > ma_previous
state = True
PERIOD = 5
bought=0
sold = 0


while state:
    EURGBP= list(get_price_history("EURGBP").values())
    # Récupérer les prix actuels (EURGBP doit être un array de prix)
    # Assure-toi que EURGBP est mis à jour à chaque boucle
    rsi_now = compute_rsi(EURGBP, 14)
    print(list(get_price_history("EURGBP").values())[-1])
    print("Rsi now" , rsi_now)
    # Vérifier conditions RSIimport matplotlib.pyplot as plt
    if rsi_now < 30 and rsi_now>10 and is_ma_increasing(EURGBP):
        # RSI < 30 → survendu → potentiellement acheter
        trade(TRADER_ID, 19000, Side.BUY)
        bought= bought +100
        print("Achat exécuté")
        
    elif rsi_now > 70 and is_ma_increasing(EURGBP) == False :
        # RSI > 70 → suracheté → potentiellement vendre
        trade(TRADER_ID, 19000, Side.SELL)
        sold = sold +100
        print("Vente exécutée")
        
    else:
        print("Bought", bought)
        print("sold", sold)
        print(moving_average(EURGBP[-10:]))
    if get_price() <= stop_loss :
                trade(TRADER_ID, 100000, Side.BUY)
                bought = bought + 10000
    if get_price() >= take_profit :
                trade(TRADER_ID, 100000, Side.SELL)
                bought = 0
    time.sleep(1) 
