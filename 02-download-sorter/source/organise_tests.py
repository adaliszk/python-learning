import os

import pytest

import organise

move_file_cases = [
    # Exception cases
    ("No target with No destination", [None, None], None, organise.MissingDestination),
    ("No target with Empty destination", [None, ""], None, organise.MissingDestination),
    ("No target with Destination", [None, "directory"], None, organise.MissingTarget),
    ("Empty target with Destination", ["", "directory"], None, organise.MissingTarget),

    # Happy cases
    ("File without extension", ["something", "directory"], ["directory/something"], None),
    ("File with extension", ["something.txt", "directory"], ["directory/something.txt"], None),
    ("File with duplicate match",
     ["something.txt", "directory"], ["directory/something.txt", "directory/something(1).txt"], None),
]


@pytest.mark.parametrize("case,params,output,exception", move_file_cases, ids=[i[0] for i in move_file_cases])
def should_move_files_and_create_destinations(case, params, output, exception, fs):
    target, directory = params

    # Check for the exception triggers
    if exception:
        with pytest.raises(exception):
            organise.move_file(target, directory)
        return

    # Iterate through the expected outputs
    for expected in output:
        # Create a dummy file
        fs.create_file(target)
        assert os.path.exists(target) is True

        # Move the file
        organise.move_file(target, directory)

        # Check what it should have happened
        assert os.path.exists(target) is False
        assert os.path.exists(expected) is True


matched_file_cases = [
    # Happy cases
    ("JPG image should be moved",
     organise.move_pictures, ["something.jpg"], ["Pictures/something.jpg"], [], None),
    ("Only JPG image should be moved",
     organise.move_pictures, ["something.jpg", "abc.txt"], ["Pictures/something.jpg"], ["abc.txt"], None),
    ("PNG image should be moved",
     organise.move_pictures, ["something.png"], ["pictures/something.png"], [], None),
    ("Only PNG image should be moved",
     organise.move_pictures, ["something.png", "abc.txt"], ["pictures/something.png"], ["abc.txt"], None),
    ("RAR file should be moved",
     organise.move_archives, ["something.rar"], ["archives/something.rar"], [], None),
    ("Only RAR file should be moved",
     organise.move_archives, ["something.rar", "abc.txt"], ["archives/something.rar"], ["abc.txt"], None),
    ("ZIP file should be moved",
     organise.move_archives, ["something.zip"], ["archives/something.zip"], [], None),
    ("Only ZIP file should be moved",
     organise.move_archives, ["something.zip", "abc.txt"], ["archives/something.zip"], ["abc.txt"], None),
    ("EXE file should be moved",
     organise.move_programs, ["something.exe"], ["programs/something.exe"], [], None),
    ("Only EXE file should be moved",
     organise.move_programs, ["something.exe", "abc.txt"], ["programs/something.exe"], ["abc.txt"], None),
    ("MSI file should be moved",
     organise.move_programs, ["something.msi"], ["programs/something.msi"], [], None),
    ("Only MSI file should be moved",
     organise.move_programs, ["something.msi", "abc.txt"], ["programs/something.msi"], ["abc.txt"], None),
    ("DOC file should be moved",
     organise.move_documents, ["something.doc"], ["documents/something.doc"], [], None),
    ("Only DOC file should be moved",
     organise.move_documents, ["something.doc", "abc.txt"], ["documents/something.doc"], ["abc.txt"], None),
    ("PDF file should be moved",
     organise.move_documents, ["something.pdf"], ["documents/something.pdf"], [], None),
    ("Only PDF file should be moved",
     organise.move_documents, ["something.pdf", "abc.txt"], ["documents/something.pdf"], ["abc.txt"], None),
    ("ODF file should be moved",
     organise.move_documents, ["something.odf"], ["documents/something.odf"], [], None),
    ("Only ODF file should be moved",
     organise.move_documents, ["something.odf", "abc.txt"], ["documents/something.odf"], ["abc.txt"], None),
    ("TORRENT file should be moved",
     organise.move_documents, ["something.torrent"], ["documents/something.torrent"], [], None),
    ("Only TORRENT file should be moved",
     organise.move_documents, ["something.torrent", "abc.txt"], ["documents/something.torrent"], ["abc.txt"], None),

]


@pytest.mark.parametrize(
    "case,matcher_function,files,moved_list,ignored_list,exception",
    matched_file_cases,
    ids=[i[0] for i in matched_file_cases]
)
def should_move_matched_files(case, matcher_function, files, moved_list, ignored_list, exception, fs):
    # TODO: Check for raised exceptions

    if exception:
        with pytest.raises(exception):
            matcher_function()

        return

    # Create the dummy files
    for file in files:
        fs.create_file(file)

        matcher_function()  # execute the move method
    matcher_function()  # Execute the move method

    for moved_file in moved_list:
        assert os.path.exists(moved_file) is True

    for ignored_file in ignored_list:
        assert os.path.exists(ignored_file) is True
