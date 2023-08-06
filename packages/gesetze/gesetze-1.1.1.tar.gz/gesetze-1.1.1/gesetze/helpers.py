from typing import Optional

import re


# One regEx to rule them all
REGEX = re.compile(r"""
    # Section sign
    (?:§+|&sect;|Art\.?|Artikel)\s*
    # Section ('Norm')
    (?P<norm>\d+(?:\w\b)?)\s*
    # Subsection ('Absatz')
    (?:(?:Abs(?:atz|\.)\s*)?(?P<absatz>(?:\d+|[XIV]+)(?:\w\b)?))?\s*
    # Sentence ('Satz')
    (?:(?:S\.|Satz)\s*(?P<satz>\d+))?\s*
    # Number ('Nummer')
    (?:(?:Nr\.|Nummer)\s*(?P<nr>\d+(?:\w\b)?))?\s*
    # Letter ('Litera')
    (?:(?:lit\.|litera|Buchst\.|Buchstabe)\s*(?P<lit>[a-z]?))?
    # Character limit
    .{0,10}?
    # Law ('Gesetz')
    (?P<gesetz>\b[A-Z][A-Za-z]*[A-Z](?:(?:\s|\b)[XIV]+)?\b)
""", re.VERBOSE)


def analyze(string: str, regex: Optional[re.Pattern] = None) -> dict:
    """
    Analyzes a single legal norm

    :param string: str Legal norm
    :param regex: re.Pattern Regex

    :return: dict Legal norm components
    """

    if regex is None:
        regex = REGEX

    match = regex.search(string)

    if not match:
        return {}

    return {k: v for k, v in match.groupdict().items() if v}


def roman2arabic(string: str) -> int:
    """
    Converts roman numerals to arabic numerals

    :param string: str Roman numeral

    :return: int Arabic numeral
    :raises: Exception Invalid character
    """

    # Transform string to uppercase
    string = string.upper()

    # If one of the characters represents an invalid roman numeral ..
    if not re.match(r'[IVXLCDM]+', string, re.IGNORECASE):
        # .. throw error
        raise Exception('Input contains invalid character!')

    # Map roman base numerals to their arabic equivalent
    romans = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000,
    }

    # Convert roman numerals to list of arabic numerals
    values = [romans[character] for character in string]

    return sum(
        val if val >= next_val else -val
        for val, next_val in zip(values[:-1], values[1:])
    ) + values[-1]
