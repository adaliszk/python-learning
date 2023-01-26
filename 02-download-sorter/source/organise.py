"""
This script implements sorting methods for your Downloads
"""
from glob import glob
from os import mkdir, rename, path, chdir


def move_file(file: str, dest: str) -> None:
    """
    Moves
    :param file: path to the old location
    :param dest: path to the new location
    :return: None
    """
    if not path.exists(dest):
        mkdir(dest)

    filename, extension = path.splitext(file)
    name = filename

    if path.exists(f"{dest}/{file}"):
        counter = 1
        while path.exists(f"{dest}/{name}"):
            name = f"{name}({str(counter)}).{extension}"
            counter += 1

    rename(file, f"{dest}/{name}")


def move_images() -> None:
    """
    Move images from your download to your pictures folder
    :return: None
    """
    images = glob("*.jpg") + glob("*.png")
    for file in images:
        move_file(file, "Pictures")


def move_documents() -> None:
    """
    Move PDF, DOC, XLS, and ODF files into your documents folder
    :return: None
    """
    documents = glob("*.pdf") + glob("*.doc*") + glob("*.odf") + glob(".torrent")
    for file in documents:
        move_file(file, "documents")


def move_archives() -> None:
    """
    Move archives like zip, rar, tgz, and tar.gz into your temp folder
    :return: None
    """
    archives = glob("*.zip") + glob("*.rar")
    for file in archives:
        move_file(file, "archives")


def move_programs() -> None:
    """
    Move programs such as exe to your temp folder
    :return: 
    """
    programs = glob("*.exe")
    for file in programs:
        move_file(file, "programs")


def categorise_downloads() -> None:
    """
    Categorise your downloaded files into images, documents, and archives
    :return: None
    """
    chdir()  # input download folder directory
    move_images()  # input download folder directory
    move_documents()  # input download folder directory
    move_archives()  # input download folder directory
    move_programs()  # input download folder directory


if __name__ == "__main__":
    categorise_downloads()
