import requests
import time

@st.cache_data(ttl=60)  # not used in FastAPI, we'll implement simple caching
_cache = {}
def fetch_current_price(ticker):
    if ticker in _cache and time.time() - _cache[ticker]['time'] < 60:
        return _cache[ticker]['price']
    url = f"https://dps.psx.com.pk/timeseries/int/{ticker}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 1 and data.get('data') and len(data['data']) > 0:
            price = data['data'][0][1]
            _cache[ticker] = {'price': float(price), 'time': time.time()}
            return float(price)
    except:
        pass
    return None

def get_live_prices(tickers):
    prices = {}
    for ticker in tickers:
        prices[ticker] = fetch_current_price(ticker)
        time.sleep(0.2)
    return prices