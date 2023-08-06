import csv
import json
import yaml
from typing import List, OrderedDict, Union


def read_csv(
    filepath: str,
    encoding: str = 'utf-8',
    newline: str = '',
    delimiter: str = ','
    ) -> List[list]:
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: a list of nested "row" lists
    """
    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        reader = csv.reader(file_obj, delimiter=delimiter)
        return [row for row in reader]


def read_csv_to_dicts(
    filepath: str,
    encoding: str ='utf-8',
    newline: str ='',
    delimiter: str =',',
    ordereddict: bool = True
    ) -> Union[List[OrderedDict], List[dict]]:
    """Accepts a file path, creates a file object, and returns a list of dictionaries
    that represent the row values using the cvs.DictReader(). Default type returned
    in list is an OrderedDict which can be overridden.

    Parameters:
        filepath (str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values
        orderdict (bool): return either list of OrderedDict objects or dict objects

    Returns:
        list: nested dictionaries representing the file contents
     """
    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        reader = csv.DictReader(file_obj, delimiter=delimiter)

        if ordereddict:
            return [row for row in reader]
        else:
            return [dict(row) for row in reader]


def read_file(
    filepath: str,
    encoding: str = 'utf-8',
    strip: bool = True
    ) -> List[str]:
    """Read text file line by line. Remove whitespace and trailing newline
    escape character.

    Parameters:
        filepath (str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file.
        strip (bool): remove white space, newline escape characters

    Returns
        list: list of lines in file
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        if strip:
            return [line.strip() for line in file_obj]
        else:
            return file_obj.readlines()


def read_json(
    filepath: str,
    encoding: str = 'utf-8'
    ) -> Union[dict, list]:
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): absolute or relative path to source file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict | list: dict or list representations of the decoded JSON document
    """
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)


def read_yaml(filepath: str) -> Union[dict, list]:
    """Read a YAML (Yet Another Markup Language) file given a valid filepath.

    Parameters:
        filepath (str): absolute or relative path to source file

    Returns:
        obj: typically a list or dictionary representation of the file object
    """
    with open(filepath, 'r') as file_object:
        return yaml.load(file_object, Loader=yaml.FullLoader)
