import datetime
import pygal
import requests

API_KEY = "ZD9X9OJCBFZXU3SJ"

def user_prompt():
    ticker_symbol = input("Please Enter a Stock Ticker Symbol: ").upper()

    chart_type = chart_input()

    chart_time_series = time_series_input()
    if chart_time_series == '1':
        intraday_interval = intraday_interval_input()
    else:
        intraday_interval = ""

    start_date = date_input_start()

    end_date = date_input_end(start_date)

    return ticker_symbol, chart_type, chart_time_series, start_date, end_date, intraday_interval

def chart_input():
    while True:
        try:
            print("\nChart Types")
            print("------------")
            print("1. Bar")
            print("2. Line\n")
            chart_type = int(input("Please Enter a Chart Type (1, 2): "))
            if chart_type not in [1, 2]:
                print("Enter a 1 or 2 for Chart Type")
            else:
                return chart_type
        except ValueError:
            print("ERROR - Enter an Integer")

def time_series_input():
    while True:
        try:
            print("\nSelect Time Series:")
            print("1. Intraday")
            print("2. Daily")
            print("3. Weekly")
            print("4. Monthly")
            chart_time_series = input("Please Enter a Time Series (1, 2, 3, 4): ")
            if chart_time_series not in ['1', '2', '3', '4']:
                print("Enter 1, 2, 3, or 4 for Time Series")
            else:
                return chart_time_series
        except ValueError:
            print("ERROR - Enter a Valid Option")


def intraday_interval_input():
    while True:
        try:
            print("\nSelect Intraday Interval:")
            print("1. 1 minute")
            print("2. 5 minutes")
            print("3. 15 minutes")
            interval = input("Please Enter an Interval (1, 2, 3): ")
            if interval not in ['1', '2', '3']:
                print("Enter 1, 2, or 3 for Interval")
            else:
                return interval
        except ValueError:
            print("ERROR - Enter a Valid Option")

def date_input_start():
    while True:
        try:
            start_date = input("\nEnter the Start Date (YYYY-MM-DD): ")
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
            return start_date
        except ValueError:
            print("ERROR - Enter a Valid Date (YYYY-MM-DD)")

def date_input_end(start_date):
    while True:
        try:
            end_date = input("\nEnter the End Date (YYYY-MM-DD): ")
            datetime.datetime.strptime(end_date, '%Y-%m-%d')
            if end_date >= start_date:
                return end_date
            else:
                print("End Date must be after Start Date.")
        except ValueError:
            print("ERROR - Enter a Valid Date (YYYY-MM-DD)")

def get_stock_data(symbol, time_series, intraday_interval):
    base_url = "https://www.alphavantage.co/query"
    function = f'TIME_SERIES_{"INTRADAY" if time_series == "1" else "DAILY"}'
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": API_KEY,
        "interval": f"{intraday_interval}min" if intraday_interval else None
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching data. Status Code: {response.status_code}")
        print(f"API Response: {response.text}")
        return None

def make_graph(stock_data, chart_type, chart_time_series, start_date, end_date):
    time_series_key = 'Time Series (1min)' if chart_time_series == '1' else 'Time Series (Daily)'
    
    if time_series_key not in stock_data:
        print(f"No data available for the specified time period: {start_date} to {end_date}")
        return
    
    ticker = stock_data['Meta Data']['2. Symbol']

    opening = []
    highs = []
    lows = []
    closing = []
    dates = []

    for date, values in stock_data[time_series_key].items():
        if start_date <= date <= end_date:
            dates.append(date)
            opening.append(float(values["1. open"]))
            highs.append(float(values["2. high"]))
            lows.append(float(values["3. low"]))
            closing.append(float(values["4. close"]))

    if not dates:
        print("There Was No Data Available For Your Input")
    else:
        chart = pygal.Line() if chart_type == 2 else pygal.Bar()
        chart.title = f'Stock Data for {ticker}: {start_date} to {end_date}'
        chart.x_labels = dates
        chart.add('Opening', opening)
        chart.add('High', highs)
        chart.add('Low', lows)
        chart.add('Closing', closing)

        chart_file_name = f"{ticker}_stock_chart.svg"
        chart.render_to_file(chart_file_name)
        print(f"Chart generated successfully. You can view it at: {chart_file_name}")

def main():
    keep_going = True
    while keep_going:
        try:
            ticker_symbol, chart_type, chart_time_series, start_date, end_date, intraday_interval = user_prompt()
            stock_data = get_stock_data(ticker_symbol, chart_time_series, intraday_interval)
            if stock_data:
                make_graph(stock_data, chart_type, chart_time_series, start_date, end_date)
            else:
                print("Error fetching stock data.")
        except Exception as e:
            print(f"Error: {e}")

        flag = input("Would you like to continue? Enter (Y/N)")
        if flag.lower() != "y":
            keep_going = False

if __name__ == '__main__':
    main()
