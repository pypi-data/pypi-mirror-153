import os
import json


def create_dir(dir_name: str):
    """
    create a directory if doesnt exists.
    :param dir_name: directory name
    :return: None
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def read_json(json_file: str) -> dict:
    """
    Reads json file from the given path
    :param json_file: json file path
    :return: json file
    """
    with open(json_file) as json_file:
        json_data = json.load(json_file)
    return json_data


def main():
    json_file = read_json(r'/petdata/input_transformations/transforms.json')
    print('brightness' in json_file.keys())


if __name__ == "__main__":
    main()