from typing import List


def process_row(row_: str | List[str]) -> str:
    """

    :param row_:
    :return:
    """
    return row_[0].strip() if isinstance(row_, List) else row_.strip()


def check_frmt_row(row_: str | List[str]) -> bool:
    """

    :param row_:
    :return:
    """
    def _check_row() -> bool:
        return process_row(row_).isdigit()

    return _check_row() if (isinstance(row_, List) and len(row_)) else (_check_row() if row_ is not None else False)
