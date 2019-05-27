import urllib
import json
import ssl
import sqlite3
import datetime
import csv
from csv import reader
from dateutil import parser
import matplotlib.pyplot as plt

URL = "https://35.204.204.210/"


def get_dates_between_2_dates(start_year, start_month, start_day, end_year, end_month, end_day):
    d1 = datetime.date(start_year, start_month, start_day)
    d2 = datetime.date(end_year, end_month, end_day)
    days = [d1 + datetime.timedelta(days=x) for x in range((d2 - d1).days + 1)]
    days_array = []
    for day in days:
        days_array.append(day.strftime('%Y-%m-%d'))
    print(days_array)
    return days_array


def create_url(date):
    url_for_request = f"{URL}{date}/"
    return url_for_request


def get_json_from_url(url):
    context = ssl._create_unverified_context()  # create ssl-non-verified context
    response = urllib.request.urlopen(url, context=context)
    data_from_url = response.read()

    try:
        json_data = json.loads(data_from_url)
    except Exception:
        json_data = None

    # get data from json
    flat_array = json_data["postings"]
    print(f"number of flats is {len(flat_array)}")
    flats = []
    if flat_array:
        for item in flat_array:
            price_usd = item["price_usd"]
            total_area = item["total_area"]
            kitchen_area = item["kitchen_area"]
            living_area = item["living_area"]
            number_of_rooms = item["number_of_rooms"]
            location = item["location"]
            added_date = item["added_on"]
            raw = (price_usd, total_area, kitchen_area, living_area, number_of_rooms, location, added_date)
            flats.append(raw)
    return flats


def create_table_in_db(db_name):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS apartments(price_usd int, total_area int, kitchen_area int, '
                       'living_area int, number_of_rooms int, location varchar(70), added_date date)')
        connection.commit()


def insert_date(db_name, params):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO apartments VALUES(?, ?, ?, ?, ?, ?, ?)', params)
        connection.commit()


def select_data_from_db(db_name):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM apartments')


def write_avg_prices_to_csv(db_name, file_name="average_prices.csv"):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT location, added_date, avg(price_usd/total_area) as avg_price FROM apartments '
                       'where location like "Шевченківський" and kitchen_area > 12 group by location, added_date')
    with open(file_name, "w", newline='') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(col[0] for col in cursor.description)
        for row in cursor:
            writer.writerow(row)


def main():
    create_table_in_db("OLX_DB.sqlite3")
    dates_array = get_dates_between_2_dates(2017, 1, 1, 2017, 12, 31)
    for date in dates_array:
        url_for_request = create_url(date)
        print(url_for_request)
        records = get_json_from_url(url_for_request)
        if records:
            for item in records:
                insert_date("OLX_DB.sqlite3", item)
    write_avg_prices_to_csv("OLX_DB.sqlite3")

    # get data from csv file
    with open('average_prices.csv', 'r') as data_file:
        data = list(reader(data_file))
        print(data)

        location = [i[0] for i in data[2:]]
        dates = [parser.parse(i[1]) for i in data[2:]]
        print(dates)
        avg_price = [float(i[2]) for i in data[2:]]

        # visualization
        plt.title('Average prices for apartments with kitchen more than 12 meters')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.plot(dates, avg_price, 'r')
        plt.show()


if __name__ == "__main__":
    main()