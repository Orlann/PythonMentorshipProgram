import matplotlib.pyplot as plt
from csv import reader
from dateutil import parser

# get data from csv file
with open('HistoricalQuotes.csv', 'r') as data_file:
    data = list(reader(data_file))

dates = [parser.parse(i[0]) for i in data[1:]]
close_price = [float(i[1]) for i in data[1:]]
open_price = [float(i[3]) for i in data[1:]]

# visualization
plt.title('EPAM Stock')
plt.xlabel('Date')
plt.ylabel('Price in USD')
plt.plot(dates, close_price, 'r')
plt.plot(dates, open_price, 'y')
plt.show()