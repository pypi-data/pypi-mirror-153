from typing import Optional


def spacer(lstring: str, rstring: str, diff_length: Optional[int] = None) -> str:
    """
    Return the combination of 2 strings w/ a constant spacing.
    The spacing character used is a white space.

    :param lstring: str
    :param rstring: str
    :param diff_length: Optional[int]
    :return: str
    """
    if diff_length is None:
        diff_length = 40

    diff_length = diff_length - len(lstring)

    res = ""
    for _ in range(diff_length):
        res += " "

    return f"{lstring}{res}{rstring}"
