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


def get_data_from_array(string_line):
    """get url, date and file size from string"""
    start_date_index = string_line.find('[')
    end_date_index = string_line.find(']')
    url = string_line[:start_date_index-1]
    date_part = string_line[start_date_index + 1: start_date_index + 12]      # date_time = item[start_date_index + 1: end_date_index]
    files_count = string_line[end_date_index + 2:]
    return url, date_part, files_count


def form_array_with_tuple(string_array):
    """form tuple from date and url as a future key in dictionary"""
    lines_with_tuple_array = []
    for line_item in string_array:
        line_with_tuple_array = []
        url, date_part, files_count = get_data_from_array(line_item)
        date_url_tuple = (date_part, url)
        line_with_tuple_array.append(date_url_tuple)
        line_with_tuple_array.append(files_count)
        lines_with_tuple_array.append(line_with_tuple_array)
    return lines_with_tuple_array


def form_dictionary_from_array(array):
    """form dictionary where key is tuple (date, url) and value is file size"""
    new_dict = {}
    for dict_item in array:
        if dict_item[0] not in new_dict:
            new_dict[dict_item[0]] = int(dict_item[1])
        else:
            new_dict[dict_item[0]] += int(dict_item[1])
    return new_dict


def convert_dictionary_to_array(dictionary):
    array_from_dictionary = []
    for key, value in dictionary.items():
        array_from_key_tuple = []
        array_without_tuple = []
        array_from_key_tuple.append(list(key))
        array_without_tuple.append(array_from_key_tuple[0][0])
        array_without_tuple.append(array_from_key_tuple[0][1])
        array_without_tuple.append(value)
        array_from_dictionary.append(array_without_tuple)
    return array_from_dictionary


def form_array_with_max_size_for_date(input_array):
    output_array = [input_array[0]]
    for i in range(1, len(input_array)):
        flag = False
        for j in range(0, len(output_array)):
            if input_array[i][0] == output_array[j][0]:
                if input_array[i][2] > output_array[j][2]:
                    output_array[j][1] = input_array[i][1]
                    output_array[j][2] = input_array[i][2]
                flag = True
                break
        if not flag:
            output_array.append(input_array[i])
    return output_array


def print_dictionary(dictionary):
    for key, value in dictionary.items():
        print(key, ": ", value)


def main():
    lines_from_file_array = get_data_from_file("log_data.txt")
    lines_from_file_array = remove_end_enter_from_sting(lines_from_file_array)
    lines_with_tuple_array = form_array_with_tuple(lines_from_file_array)
    dict_with_total_file_count_for_date_and_url = form_dictionary_from_array(lines_with_tuple_array)
    date_url_total_count = convert_dictionary_to_array(dict_with_total_file_count_for_date_and_url)
    max_size_for_date_array = form_array_with_max_size_for_date(date_url_total_count)

    for item in max_size_for_date_array:
        print(item[0], " - ", item[1])


if __name__ == "__main__":
    main()
