from typing import List


def process_row(row_: str | List[str]) -> str:
    """
    Process and clean a row.
    :param row_: A string or a list of strings.
    :return: Cleaned row.
    """
    return row_[0].strip() if isinstance(row_, List) else row_.strip()


def check_frmt_row(row_: str | List[str]) -> bool:
    """
    Check if a row is valid.
    :param row_: A string or a list of strings.
    :return: True if the row is valid, False otherwise.
    """
    if (isinstance(row_, List) and len(row_)) or isinstance(row_, str):
        return process_row(row_).isdigit()
    else:
        return False
