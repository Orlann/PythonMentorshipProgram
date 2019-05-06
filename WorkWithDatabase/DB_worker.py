import requests
import sqlite3
import csv

DB_NAME = 'forex.sqlite3'


def get_currency_from_site(url):
    response_json = requests.get(url).json()
    currency_dict = response_json['rates']
    return currency_dict


def get_currencies_codes_from_db(db_name):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        currency_codes_from_db = cursor.execute('SELECT currency_code FROM rates').fetchall()
        codes_from_db = set()
        for item in currency_codes_from_db:
            codes_from_db.add(item[0])
        return codes_from_db


def get_currency_rate_from_db(db_name, currency_code):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        param = (currency_code,)
        result = cursor.execute('SELECT * FROM rates WHERE currency_code = ?', param)
        rate = cursor.fetchall()
        return rate


def update_date(db_name, currency_code, currency_rate):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        param = (currency_rate, currency_code)
        cursor.execute('UPDATE rates SET rate = ? WHERE currency_code = ?', param)
        connection.commit()


def insert_date(db_name, currency_code, currency_rate):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        param = (currency_code, currency_rate)
        cursor.execute('INSERT INTO rates VALUES(?, Null, ?)', param)
        connection.commit()


def delete_data(db_name, currency_code):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        param = (currency_code,)
        cursor.execute('DELETE FROM rates WHERE currency_code = ?', param)
        connection.commit()


def select(db_name):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM rates')
        for row in cursor.fetchall():
            print(row)


def write_to_csv(file_name="output.csv", db_name=DB_NAME):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM rates')
        with open(file_name, "w") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(col[0] for col in cursor.description)
            for row in cursor:
                writer.writerow(row)


def main():
    # ------- Get data from web
    currency_dict = get_currency_from_site('https://api.exchangeratesapi.io/latest')
    currency_codes_list = set(currency_dict.keys())

    # ------- Removing absent currencies from database
    currency_from_db_list = get_currencies_codes_from_db(DB_NAME)
    absent_currencies = currency_from_db_list - currency_codes_list
    for currency in absent_currencies:
        delete_data(DB_NAME, currency)
    
    # ------- Inserting new currencies and updating rates
    for key, value in currency_dict.items():
        curr_info = get_currency_rate_from_db(DB_NAME, key)
        if not curr_info:
            insert_date(DB_NAME, key, value)
        else:
            rate = curr_info[0][2]
            if value != rate:
                update_date(DB_NAME, key, value)

    write_to_csv()


if __name__ == "__main__":
    main()
