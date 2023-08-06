from typing import Optional, Union


def load_json(json_file: str) -> dict:
    """
    Loads data from JSON file

    :param json_file: str Path to JSON file

    :return: dict Loaded JSON data
    :raises: Exception Error decoding JSON
    """

    from json import load
    from json.decoder import JSONDecodeError

    try:
        with open(json_file, 'r') as file:
            return load(file)

    except JSONDecodeError:
        raise Exception

    return {}


def dump_json(data: Union[dict, list], json_file: str, indent: Optional[int] = None, ensure_ascii: bool = False) -> None:
    """
    Dumps data to JSON file

    :param data: dict | list Data to be dumped
    :param json_file: str Path to JSON file
    :param indent: int Indent (default: None)
    :param ensure_ascii: bool Whether to encode ASCII symbols

    :return: None
    """

    from json import dump

    with open(json_file, 'w') as file:
        dump(data, file, indent = indent, ensure_ascii = ensure_ascii)


def create_path(path: str) -> None:
    """
    Creates path recursively

    :param path: str Path to directory / file

    :return: None
    """

    from os import makedirs
    from os.path import exists

    # If path does not exist ..
    if not exists(path):
        # .. attempt to ..
        try:
            # .. create it
            makedirs(path)

        # Guard against race condition
        except OSError:
            pass
