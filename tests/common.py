"""Define common test utilities."""
import os

TEST_TOKEN = "abcde12345"  # noqa: S105
TEST_URL = "http://127.0.0.1:8000"


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
        filename: The filename of the fixtures/ file to load.

    Returns:
        A string containing the contents of the file.
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
