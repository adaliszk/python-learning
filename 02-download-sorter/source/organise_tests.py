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


def should_call_categorise_methods():
    move_pictures = mocker.patch("move_pictures")
    move_pictures.return_value = None


organise.categorise_downloads()
