import csv
import json
import requests
from typing import List, Tuple, Union


def write_csv(
    filepath: str,
    data: Union[list, tuple],
    headers: Union[list, tuple] = None,
    encoding: str = 'utf-8',
    newline: str = ''
    ) -> None:
    """
    Writes data to a target CSV file. Column headers are written as the first
    row of the CSV file if optional headers are specified.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted
    fields may not be interpreted correctly by the csv.reader. On platforms that utilize
    `\r\n` an extra `\r` will be added.

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list | tuple): sequence to be written to the target file
        headers (seq): optional header row list or tuple
        encoding (str): name of encoding used to encode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences

    Returns:
        None
    """
    with open(filepath, 'w', encoding=encoding, newline=newline) as file_obj:
        writer = csv.writer(file_obj)
        if headers:
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)
        else:
            writer.writerows(data)


def write_dicts_to_csv(
    filepath: str,
    data: List[dict],
    fieldnames: Union[list, tuple],
    encoding: str ='utf-8',
    newline: str = ''
    ) -> None:
    """
    Writes dictionary data to a target CSV file as row data using the csv.DictWriter().
    The passed in fieldnames list is used by the DictWriter() to determine the order
    in which each dictionary's key-value pairs are written to the row.

    WARN: This function is not designed to handle dictionaries that include key-value
    pairs in which the values are sequences or dictionaries. In such cases, serialize the
    object as JSON and write to a file using < write.write_json >.

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list): dictionary content to be written to the target file
        fieldnames (seq): sequence specifing order in which key-value pairs are written to each row
        encoding (str): name of encoding used to encode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences

    Returns:
        None
    """
    with open(filepath, 'w', encoding=encoding, newline=newline) as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)

        writer.writeheader() # first row
        writer.writerows(data)
        # for row in data:
        #     writer.writerow(row)


def write_file(
    filepath: str,
    data: Union[List[str], Tuple[str]],
    encoding: str = 'utf-8',
    newline: bool = True
    ) -> None:
    """Write content to a target file encoded as UTF-8. If optional newline is specified
    append each line with a newline escape sequence (`\n`).

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list | tuple): sequence of strings comprising the content to be written to the
                             target file
        encoding (str): name of encoding used to encode the file.
        newline (bool): add newline escape sequence to line

    Returns:
        None
    """
    with open(filepath, 'w', encoding=encoding) as file_obj:
        if newline:
            for line in data:
                file_obj.write(f"{line}\n") # add newline
        else:
            file_obj.writelines(data) # write sequence to file


def write_file_response_chunked(
    filepath: str,
    response: requests.Response,
    mode: str = 'w',
    chunk_size: int = 1024
    ) -> None:
    """Writes < requests.Response > to a target file as a stream of data chunks.
    Override the optional write mode value if binary content <class 'bytes'> is to
    be written to file (i.e., mode='wb') or an append operation is intended on an
    existing file (i.e., mode='a' or 'ab').

    Parameters:
        filepath (str): absolute or relative path to target file
        response (requests.Response): data to be written to the target file
        mode (str): write operation mode
        chunk_size (int); size of data chunks to stream

    Returns:
        None
    """
    with open(filepath, mode) as file_object:
        for chunk in response.iter_content(chunk_size=chunk_size):
            file_object.write(chunk)


def write_json(
    filepath: str,
    data: Union[dict, list],
    encoding: str = 'utf-8',
    ensure_ascii: bool = False,
    indent: int = 2
    ) -> None:
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict | list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """
    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)
