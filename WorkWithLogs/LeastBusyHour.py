import re


def get_data_from_file(file_name):
    file_lines_array = []
    with open(file_name, "r") as read_file:
        for line in read_file:
            file_lines_array.append(line)
    return file_lines_array


def remove_end_enter_from_sting(array):
    pattern = r"\n"
    new_array = []
    for item in array:
        item = re.sub(pattern, "", item)
        new_array.append(item)
    return new_array


def get_data_from_string(string_line):
    start_date_index = string_line.find('[')
    end_date_index = string_line.find(']')
    hour_part = string_line[start_date_index + 1: start_date_index + 15]
    files_count = string_line[end_date_index + 2:]
    return hour_part, files_count


def form_array_with_data(input_array):
    output_array = []
    for line_item in input_array:
        output_array_element = []
        hour_part, files_count = get_data_from_string(line_item)
        output_array_element.append(hour_part)
        output_array_element.append(files_count)
        output_array.append(output_array_element)
    return output_array


def form_busy_hour_dictionary(input_array):
    output_dictionary = {}
    count = 0
    for item in input_array:
        if item[0] not in output_dictionary:
            output_dictionary[item[0]] = 1
        else:
            count += 1
            output_dictionary[item[0]] = count
    return output_dictionary


def convert_dictionary_to_array(dictionary):
    array_from_dictionary = []
    for key, value in dictionary.items():
        array = [key, value]
        array_from_dictionary.append(array)
    return array_from_dictionary


def print_dictionary(dictionary):
    for key, value in dictionary.items():
        print(key, ": ", value)


def get_least_busy_hours_from_array(input_array):
    output_array = [input_array[0]]
    for item in range(1, len(input_array)):
        if input_array[item][1] <= output_array[0][1]:
            output_array.append(input_array[item])
    return output_array


def format_hour(item):
    date = item[:len(item)-3]
    hour = item[-2:]
    string = "{} - {} hour".format(date, hour)
    return string


def main():
    lines_from_file_array = get_data_from_file("log_data.txt")
    lines_from_file_array = remove_end_enter_from_sting(lines_from_file_array)
    data_array = form_array_with_data(lines_from_file_array)
    hours_busyness_dictionary = form_busy_hour_dictionary(data_array)
    hours_busyness_array = convert_dictionary_to_array(hours_busyness_dictionary)
    least_busy_hours = get_least_busy_hours_from_array(hours_busyness_array)

    print("The least busy hours:")
    for item in least_busy_hours:
        print(format_hour(item[0]))


if __name__ == "__main__":
    main()
