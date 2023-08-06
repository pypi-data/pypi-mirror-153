#!/usr/bin/python
import os
import logging
import sys
import shutil
from pathlib import Path


def read_file(file: str) -> str:
    """Read a file content

    Parameters
    ----------
    file : str
        path to the file

    Returns
    -------
    str
        A string with the file content
    """
    with open(file, "r") as file:
        private_key = file.read()
    return private_key


def file_print(
    content, file: str, mode: str = "write", sep: str = " ", end: str = "\n", **kwargs
) -> None:
    """Print the content to file

    Parameters
    ----------
    content : _type_
        Content to be printed
    file : str
        path to the file
    mode : str, optional
        Write mode. Can be 'write' or 'append', by default "write"
    sep : str, optional
        String inserted between values, by default " "
    end : str, optional
        String appended after the last value, by default "\n"
    """

    if mode == "write":
        mode = "w"

    elif mode == "append":
        mode = "a"

    with open(file, mode) as text_file:
        print(content, file=text_file, sep=sep, end=end, **kwargs)


def make_directory(path: str, parents: bool = True, exist_ok: bool = True) -> None:
    """Creates a directory if it does not exists.

    Parameters
    ----------
    path : str
        Path to new directory
    parents : bool, optional
        If parents is True, any missing parents of this path are created as needed, by default True
    exist_ok : bool, optional
        If exist_ok is false (the default), FileExistsError is raised if the target directory already exists., by default True
    """

    try:
        if parents:
            Path(path).mkdir(parents=parents, exist_ok=exist_ok)

        else:
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                logging.error(f"Directory '{path}' not found")

    except Exception as err:
        logging.error(err)


def remove_file(file_path: str) -> None:
    """Remove the file from a specified path

    Parameters
    ----------
    file_path : str
        Path to the file
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)

        except Exception as err:
            logging.error(err)
    else:
        logging.error(f"File '{file_path}' not found")


def remove_empty_directory(folder_path: str) -> None:
    """Remove a directory if it is empty

    Parameters
    ----------
    folder_path : str
        Path to the directory
    """
    if os.path.exists(folder_path):
        if len(os.listdir(folder_path)) == 0:
            try:
                os.rmdir(folder_path)

            except Exception as err:
                logging.error(err)
        else:
            logging.error(f"Folder '{folder_path}' is not empty")
    else:
        logging.error(f"Directory '{folder_path}' not found")


def remove_directory_recursively(folder_path):
    """Remove a directory even if it is not empty

    Parameters
    ----------
    folder_path : str
        Path to the directory
    """

    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
        except Exception as err:
            logging.error(err)
    else:
        logging.error(f"Directory '{folder_path}' not found")


def remove_directory(folder_path, recursive: bool = False) -> None:

    """Remove a directory with option of recusivity

    Parameters
    ----------
    folder_path : str
        Path to the directory
    recursive : bool, optional
        True if remove folder recursively, by default False
    """
    if recursive:
        remove_directory_recursively(folder_path)
    else:
        remove_empty_directory(folder_path)
