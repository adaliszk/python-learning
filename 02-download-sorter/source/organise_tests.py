import pytest
import os

from organise import MissingTarget, MissingDestination, move_file

move_file_cases = [
    # Exception cases
    ("No target with No destination", [None, None], None, MissingDestination),
    ("No target with Empty destination", [None, ""], None, MissingDestination),
    ("No target with Destination", [None, "directory"], None, MissingTarget),
    ("Empty target with Destination", ["", "directory"], None, MissingTarget),

    # Happy cases
    ("File without extension", ["something", "directory"], ["directory/something"], None),
    ("File with extension", ["something.txt", "directory"], ["directory/something.txt"], None),
    ("File with duplicate match", ["something.txt", "directory"],
     ["directory/something.txt", "directory/something(1).txt"], None),
]


@pytest.mark.parametrize("case,params,output,exception", move_file_cases, ids=[i[0] for i in move_file_cases])
def should_move_files_and_create_destinations(case, params, output, exception, fs):
    target, directory = params

    # Check for the exception triggers
    if exception:
        with pytest.raises(exception):
            move_file(target, directory)
        return

    # Iterate through the expected outputs
    for expected in output:
        # Create a dummy file
        fs.create_file(target)
        assert os.path.exists(target) is True

        # Move the file
        move_file(target, directory)
        assert os.path.exists(expected) is True
        assert os.path.exists(target) is False
