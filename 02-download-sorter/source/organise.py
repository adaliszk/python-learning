"""
This script implements sorting methods for your Downloads
"""
from glob import glob
import os


def move_file(src: str, dest: str) -> None:
    """
    Moves
    :param src: path to the old location
    :param dest: path to the new location
    :return: None
    """


def move_images() -> None:
    """
    Move images from your download to your pictures folder
    :return: None
    """
    images = glob("*.jpg") + glob("*.png")
    for file in images:
        print(f"Moving image: {file}")


def move_documents() -> None:
    """
    Move PDF, DOC, XLS, and ODF files into your documents folder
    :return: None
    """
    documents = glob("*.pdf") + glob("*.doc*") + glob("*.odf")
    for file in documents:
        print(f"Moving document: {file}")


def move_archives() -> None:
    """
    Move archives like zip, rar, tgz, and tar.gz into your temp folder
    :return: None
    """
    archives = glob("*.zip") + glob("*.rar")
    for file in archives:
        print(f"Moving archives: {file}")


def categorise_downloads() -> None:
    """
    Categorise your downloaded files into images, documents, and archives
    :return: None
    """
    os.chdir("/mnt/c/Users/adaliszk/Downloads")
    move_images()
    move_documents()
    move_archives()


if __name__ == "__main__":
    categorise_downloads()
