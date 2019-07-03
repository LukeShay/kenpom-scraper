def tuple_to_string(given_tuple: tuple) -> tuple:
    string = ''
    for s in given_tuple:
        string += str(s) + ' '

    return string


def write_to_file_and_print(file, string):
    file.write(string + '/n')
    print(string)
