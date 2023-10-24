import requests

API_KEY = "ZD9X9OJCBFZXU3SJ"

def generate_alpha_vantage_link(symbol):
    base_url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_INTRADAY"
    interval = "1min"
    api_key = API_KEY

    params = {
        "function": function,
        "symbol": symbol,
        "interval": interval,
        "apikey": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.url
    else:
        return f"Error: Unable to generate the link. Status code: {response.status_code}"

# Example usage for Google's stock (symbol: GOOGL)
symbol = "GOOGL"
link = generate_alpha_vantage_link(symbol)
print("Alpha Vantage Link for Google's Stock Today:")
print(link)
