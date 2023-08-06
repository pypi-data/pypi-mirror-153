import re

from typing import List, Union


def get_hash(filename: str) -> str:
    """
    Extracts file hash from filename

    :param filename: str Filename

    :return: str File hash
    """

    # Define file hash pattern
    pattern = r'\.(\w*)\.\w{2,4}$'

    # Attempt to ..
    try:
        # .. match filename & extract file hash
        return re.search(pattern, filename, re.IGNORECASE).group(1)

    # .. otherwise ..
    except:
        # .. return empty string
        return ''


def is_allowed(extension: str, extensions: Union[List[str], str]) -> bool:
    """
    Checks whether file extension is allowed

    :param extension: str File extension to be tested
    :param extensions: list | str File extensions to test against

    :return: bool Whether file extension is allowed
    """

    # No extensions ..
    if not extensions:
        # .. anything goes
        return True

    # Lowercase allowed extensions ..
    # (1) .. being passed as list
    if isinstance(extensions, list):
        extensions = [extension.lower() for extension in extensions]

    # (2) .. being passed as string
    if isinstance(extensions, str):
        extensions = extensions.lower()

    # Check whether given extension is allowed after ..
    # (1) .. stripping any dot on the left (eg '.txt' becomes 'txt')
    # (2) .. lowercasing it
    return extension.lstrip('.').lower() in extensions
