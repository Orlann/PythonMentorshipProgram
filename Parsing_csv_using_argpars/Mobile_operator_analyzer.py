import re
import csv
import argparse


def get_data_from_file(file_name):
    try:
        with open(file_name, encoding="utf8") as file:
            file_text = file.read()
            return file_text
    except IOError:
        print("Error with file")


def get_phones_from_text(text):
    # pattern = r"(\+38)?0? ?\(?\d?\(?\d{2}\)? ?\d{3}-?\d{2}-?\d{2}"
    pattern = "0? ?\(?\d?\(?\d{2}\)? ?\d{3}-?\d{2}-?\d{2}"
    phones_array = re.findall(pattern, text)
    for i in range(0, len(phones_array)):
        pattern_for_removing = "[ ()]"
        phones_array[i] = re.sub(pattern_for_removing, "", phones_array[i])
    return phones_array


def get_operators(file_name):
    with open(file_name, newline='', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        array = []
        for row in reader:
            array.append(row)
    return array


def remove_redundant_symbol_from_operator(operator_array):
    for i in range(0, len(operator_array)):
        pattern_for_removing = "[ x]"
        operator_array[i][0] = re.sub(pattern_for_removing, "", operator_array[i][0])
    return operator_array[1:]


def get_operator_cods(operator_name, operator_array):
        operator_cods = []
        for item in operator_array:
            if item[1] == operator_name:
                operator_cods.append(item[0])
        return operator_cods


def compare_number_with_operator(operator, operator_cods, phones_array):
    result_phones = []
    flag = False
    for phone in phones_array:
        for cod in operator_cods:
            if phone[1] == '8':
                if phone[1:4] == cod:
                    array_element = [phone, operator]
                    result_phones.append(array_element)
                    flag = True
                    break
            elif phone[1:3] == cod:
                array_element = [phone, operator]
                result_phones.append(array_element)
                flag = True
                break
    return result_phones


def write_to_csv(file_name, writed_item):
    with open (file_name, "w", newline="") as file_to_write:
        writer = csv.writer(file_to_write, quoting = csv.QUOTE_ALL)
        writer.writerow(['Number', 'Provider'])
        writer.writerows(writed_item)


def main():
    parser = argparse.ArgumentParser(description='Input information about phones and mobile operators')
    parser.add_argument('-i', '--inputfile', help='Input name of income file')
    parser.add_argument('-c', '--csvfile', help='Input name of csv file')
    parser.add_argument('-p', '--operatorname', help='Input name of operator')
    parser.add_argument('-o', '--outputfile', help='Input name of outcome file')
    args = parser.parse_args()
    input_file = args.inputfile
    csv_file = args.csvfile
    operator = args.operatorname
    output_file = args.outputfile

    text_with_phones = get_data_from_file(input_file)
    phones_array = get_phones_from_text(text_with_phones)
    operator_array = get_operators(csv_file)
    operator_array = remove_redundant_symbol_from_operator(operator_array)
    operator_cods = get_operator_cods(operator, operator_array)
    result_phones = compare_number_with_operator(operator, operator_cods, phones_array)
    write_to_csv(output_file, result_phones)


if __name__ == "__main__":
    main()
