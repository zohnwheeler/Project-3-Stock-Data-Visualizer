import requests
import pygal
from datetime import datetime
from pygal.style import CleanStyle
from urllib.parse import quote
import os

# Function to query Alpha Vantage API and fetch stock data
def get_stock_data(symbol, function, start_date, end_date):
    api_key = "ZD9X9OJCBFZXU3SJ" 
    base_url = "https://www.alphavantage.co/query"
    
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Filter data based on date range
        filtered_data = {}
        for date, values in data["Time Series (Daily)"].items():
            if start_date <= date <= end_date:
                filtered_data[date] = values
        return filtered_data
    else:
        print(f"Error fetching data. Status Code: {response.status_code}")
        return None

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
        return None
    
    chart.title = f"{symbol} Stock Prices"
    chart.x_labels = dates
    chart.add("Close Price", closing_prices)
    
    chart_file_name = f"{symbol}_stock_chart.svg"
    try:
        chart.render_to_file(chart_file_name)
        print(f"Chart saved as {chart_file_name}")
        # Return the file path of the saved chart
        return os.path.abspath(chart_file_name)
    except Exception as e:
        print(f"Error saving chart: {e}")
        return None

# Main function to get user input and generate the chart
def main():
    print("Welcome to the Stock Chart Generator!")
    symbol = input("Enter the stock symbol: ")
    options = ["Line Chart", "Bar Chart"]
    chart_type = get_user_choice(options, "Please enter the corresponding number for the chart type: ")  # User selects 1 for Line Chart, 2 for Bar Chart
    functions = ["TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"]
    function = functions[get_user_choice(functions, "Please enter the corresponding number for the time series function: ") - 1]  # User selects 1 to 3 for the time series function
   
    # ...
    start_date = None
    end_date = None
    
    # Get start and end dates, ensuring end date is not before start date
    while True:
        start_date_input = input("Enter the start date (YYYY-MM-DD): ")
        end_date_input = input("Enter the end date (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
            if start_date <= end_date:
                break
            else:
                print("End date cannot be before start date. Please enter valid dates.")
        except ValueError:
            print("Invalid date format. Please enter dates in YYYY-MM-DD format.")
    
    stock_data = get_stock_data(symbol, function, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    if stock_data:
        chart_file_path = generate_chart(stock_data, chart_type, symbol)
        if chart_file_path:
            # Output the URL for the user to click on
            chart_url = quote(chart_file_path)  # URL-encode the file path
            print(f"Chart URL: file://{chart_url}")
        
    

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

if __name__ == "__main__":
    main()
