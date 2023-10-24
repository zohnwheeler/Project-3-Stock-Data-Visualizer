import requests
import pygal
from datetime import datetime
from pygal.style import CleanStyle

# Function to query Alpha Vantage API and fetch stock data
def get_stock_data(symbol, function, start_date, end_date):
    api_key = "ZD9X9OJCBFZXU3SJ"
    base_url = "https://www.alphavantage.co/query"
    
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full",  # Retrieve full historical data
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        print(f"Error fetching data. Status Code: {response.status_code}")
        return None

    data = response.json()

    if "Time Series (Daily)" not in data:
        print("Invalid stock symbol or no data available for the given symbol.")
        return None
    
    # Filter data based on date range
    filtered_data = {}
    for date, values in data["Time Series (Daily)"].items():
        if start_date <= date <= end_date:
            filtered_data[date] = values
    
    return filtered_data

# Function to generate and render the chart using Pygal
def generate_chart(stock_data, chart_type, symbol):
    dates = []
    closing_prices = []
    for date, values in stock_data.items():
        dates.append(datetime.strptime(date, "%Y-%m-%d"))
        closing_prices.append(float(values["4. close"]))
    
    if chart_type == 1:  # 1 corresponds to Line Chart
        chart = pygal.Line(style=CleanStyle, x_label_rotation=45)
    elif chart_type == 2:  # 2 corresponds to Bar Chart
        chart = pygal.Bar(style=CleanStyle, x_label_rotation=45)
    else:
        print("Invalid chart type selected.")
        return
    
    chart.title = f"{symbol} Stock Prices"
    chart.x_labels = dates
    chart.add("Close Price", closing_prices)
    
    try:
        chart.render_to_file("stock_chart.svg")
        print("Chart saved as stock_chart.svg")
    except Exception as e:
        print(f"Error saving chart: {e}")

# Function to display menu and get user choice
def get_user_choice(options, message):
    while True:
        print("\nOptions:")
        for index, option in enumerate(options, start=1):
            print(f"{index}. {option}")
        choice = input(message)
        try:
            choice = int(choice)
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Main function to get user input and generate the chart
def main():
    print("Welcome to the Stock Chart Generator!")
    symbol = input("Enter the stock symbol: ")
    options = ["Line Chart", "Bar Chart"]
    chart_type = get_user_choice(options, "Please enter the corresponding number for the chart type: ")  # User selects 1 for Line Chart, 2 for Bar Chart
    functions = ["TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY", "TIME_SERIES_INTRADAY"]
    function = functions[get_user_choice(functions, "Please enter the corresponding number for the time series function: ") - 1]  # User selects 1 to 4 for the time series function
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
        return
    
    stock_data = get_stock_data(symbol, function, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if stock_data:
        generate_chart(stock_data, chart_type, symbol)

if __name__ == "__main__":
    main()
