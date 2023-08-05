import os
import pathlib


def get_content_definition_file_path():
    my_folder = pathlib.Path(__file__).parent.absolute()
    return os.path.join(my_folder, get_content_definition_file())


def get_content_definition_file():
    return "ws_content_type_definitions.json"
