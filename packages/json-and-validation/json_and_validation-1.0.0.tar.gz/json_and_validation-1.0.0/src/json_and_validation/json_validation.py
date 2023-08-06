# json_validation.py
import os
import json


def is_valid_json_string(json_string_to_test: str) -> bool:
    """ Returns True if json_string_to_test represents valid JSON syntax,
    False otherwise. """
    try:
        json.loads(json_string_to_test)
    except ValueError as err:
        print(err)
        return False
    return True


def is_valid_json_file(json_file_to_test: str) -> bool:
    """ Returns True if json_file_to_test contains valid JSON syntax,
    False otherwise. """
    if os.path.isfile(json_file_to_test):
        file_to_string = ""
        with open(json_file_to_test, 'r') as json_file:
            for line in json_file:
                file_to_string += line
        return is_valid_json_string(file_to_string)
    else:
        print(" > Input file %s does not exist." % json_file_to_test)


if __name__ == "__main__":
    print("Running json_validation.py directly.")
    INPUT_JSON_FOLDER = "./data/json/input/"
    files_to_validate = [
        INPUT_JSON_FOLDER + filename
        for filename in os.listdir(INPUT_JSON_FOLDER)
    ]
    print("Discovered %s files." % len(files_to_validate))

    print()
    print("  ++  Section 1: JSON file validation  ++")
    for file_to_validate in files_to_validate:
        print()
        print("File: %s" % file_to_validate)
        print(" > is_valid_json_file: ",
              is_valid_json_file(file_to_validate))

    print()
    print("  ++  Section 2: JSON string validation  ++")
    for file_to_validate in files_to_validate:
        print()
        print("File: %s" % file_to_validate)
        string_to_validate = ""
        with open(file_to_validate, 'r') as f_to_validate:
            for line_to_validate in f_to_validate:
                string_to_validate += line_to_validate
            print(" > is_valid_json_string: ",
                  is_valid_json_string(string_to_validate))

    print()
    print("End of json_validation.py")
