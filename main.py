import datetime
import pygal
import re
import requests

API_KEY = "ZD9X9OJCBFZXU3SJ"

def userPrompt():
    tickerSymbol = input("Please Enter a Stock Ticker Symbol: ").upper()
    chartType = chartInput()
    chartTimeSeries = timeSeriesInput()
    if chartTimeSeries == 1:
        intradayInterval = intradayIntervalInput()
    else:
        intradayInterval = ""
    startDate = dateInputStart()
    endDate = dateInputEnd(startDate)
    return (tickerSymbol, chartType, chartTimeSeries, startDate, endDate, intradayInterval)

def chartInput():
    while True:
        try:
            print("\nChart Types")
            print("------------")
            print("1. Bar")
            print("2. Line\n")
            chartType = int(input("Please Enter a Chart Type (1, 2): "))
            if chartType not in [1, 2]:
                print("Enter a 1 or 2 for Chart Type")
            else:
                return chartType
        except ValueError:
            print("ERROR - Enter an Integer")

def timeSeriesInput():
    while True:
        try:
            print("\nSelect the Time Series of the chart you want to Generate")
            print("---------------------------------------------------------")
            print("1. Intraday")
            print("2. Daily")
            print("3. Weekly")
            print("4. Monthly\n")
            chartTimeSeries = int(input("Please Enter a Chart Time Series(1, 2, 3, 4): "))
            if chartTimeSeries not in [1, 2, 3, 4]:
                print("Enter a 1, 2, 3, or 4 for Chart Time Series")
            else:
                return chartTimeSeries
        except ValueError:
            print("ERROR - Enter an Integer")

def intradayIntervalInput():
    while True:
        try:
            print("\nSelect the Interval of the Intraday graph you want to Generate")
            print("---------------------------------------------------------")
            print("1. 1 minute")
            print("2. 5 minute")
            print("3. 15 minute")
            print("4. 30 minute")
            print("5. 60 minute\n")
            intradayInterval = int(input("Please Enter an Intraday Interval(1, 2, 3, 4, 5): "))
            if intradayInterval not in [1, 2, 3, 4, 5]:
                print("Enter a 1, 2, 3, 4, or 5 for Intraday Interval")
            else:
                return intradayInterval
        except ValueError:
            print("ERROR - Enter an Integer")

def dateNotInTheFuture(date_info):
    currentDate = datetime.date.today().strftime('%Y-%m-%d')
    try:
        if validate(date_info):
            if datetime.datetime.strptime(currentDate, '%Y-%m-%d') > datetime.datetime.strptime(date_info, '%Y-%m-%d'):

                return date_info
            else:
                raise Exception
    except Exception:
        print("ERROR - Please Enter a Date That is In The Past - dateNotInTheFuture()")

def dateInputStart():
    while True:
        try:
            startDate = input("\nEnter the Start Date (YYYY-MM-DD): ")
            if dateNotInTheFuture(startDate):
                return startDate
        except ValueError:
            print("ERROR - Enter a Valid Date")

def dateInputEnd(startDate):
    while True:
        try:
            endDate = input("\nEnter the End Date (YYYY-MM-DD): ")
            if dateNotInTheFuture(endDate):
                if endDate >= startDate:
                    return endDate
                else:
                    print("The End Date Must be After The Start Date")
        except ValueError:
            print("ERROR - Enter a Valid Date")

def validate(date_info):
    try:
        dateRegex = '^[0-9]{4}.(1[0-2]|0[1-9]).(3[01]|[12][0-9]|0[1-9])'
        if re.search(dateRegex, date_info):
            datetime.datetime.strptime(date_info, '%Y-%m-%d')
            return True
        else:
            raise ValueError
    except ValueError:
        print("ERROR - Incorrect data format: should be YYYY-MM-DD - Validate()")

def makeGraph(data, chartType, startDate, endDate):
    chart = None
    if chartType == 1:
        chart = pygal.Bar(x_label_rotation=-45, x_labels_major_every=1, show_minor_x_labels=False)
    elif chartType == 2:
        chart = pygal.Line(x_label_rotation=-45, x_labels_major_every=1, show_minor_x_labels=False)
    else:
        print("Invalid Chart Type")
        return

    chart.title = 'Stock Data Trends'
    dates = []
    opening = []
    highs = []
    lows = []
    closing = []

    for date in sorted(data.keys()):
        if startDate <= date <= endDate:
            dates.append(date)
            opening.append(float(data[date]["1. open"]))
            highs.append(float(data[date]["2. high"]))
            lows.append(float(data[date]["3. low"]))
            closing.append(float(data[date]["4. close"]))

    # If no data is available for the specified date range, inform the user
    if not dates:
        print("No data available for the specified date range.")
        return

    # Reverse the lists to maintain chronological order
    dates.reverse()
    opening.reverse()
    highs.reverse()
    lows.reverse()
    closing.reverse()

    chart.x_labels = dates
    chart.add('Opening', opening)
    chart.add('High', highs)
    chart.add('Low', lows)
    chart.add('Closing', closing)

    # Generate the graph as an SVG file
    chart.render_to_file('stock_chart.svg')
    print("Graph generated successfully.")

    return chart


def getJsonPage():
    info = userPrompt()
    symbol, chartType, chartTimeSeries, chartStartDate, chartEndDate, intraDayInfo = info

    if chartTimeSeries == 1:
        intraDayInfo = "&interval=1min"
    elif chartTimeSeries == 2:
        intraDayInfo = ""

    chartTimeSeries = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"][chartTimeSeries - 1]

    baseLink = "https://www.alphavantage.co/query?"
    queryData = f"function={chartTimeSeries}&symbol={symbol}{intraDayInfo}&apikey={API_KEY}"

    req = requests.get(baseLink + queryData)
    data = req.json()

    if 'Invalid API call' not in req.text:
        makeGraph(data, chartType, chartStartDate, chartEndDate)

    else:
        print("The Ticker You Entered is Not in The API\n")
        


def main():
    keepGoing = True
    while keepGoing:
        getJsonPage()
        flag = input("Would you like to continue? Enter (Y/N)")
        if flag.lower() != "y":
            keepGoing = False


if __name__ == '__main__':
    main()
