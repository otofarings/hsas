import csv
import os
from typing import List, Any, IO

from config import NUM_START_WITH

APPEND_OPT = "a"
READ_OPT = "r"
WRITE_OPT = "w"

CSV_TYPE = ".csv"
TXT_TYPE = ".txt"
UIDS_TYPE = ".uids"
STABLE_TYPE = ".stable"


def create_dir(path_: str) -> None:
    """
    Creating a folder on the passed path.

    :param path_: A string containing the path to the new folder.
    :return:
    """
    if not os.path.exists(path_):
        os.mkdir(path_)


def delete_file(file_path_: str) -> None:
    """

    :param file_path_:
    :return:
    """
    if os.path.exists(file_path_):
        os.remove(file_path_)


def check_file(path_: str) -> bool:
    """
    Check the file configurations to see if it can be processed.

    Basic conditions:

    - The file exists in the system;
    - The file does not start with a dot;
    - The file extension is on the list of files available for processing.

    :param path_: A string containing the path to the file.
    :return: True if the file has suitable configurations, otherwise False.
    """
    file_name = os.path.basename(path_)  # Get the file name from the path to it.
    return file_name.endswith((TXT_TYPE, CSV_TYPE)) and not file_name.startswith(".") and os.path.exists(path_)


def get_files_lst_in_dir(fold_path_: str) -> List[str]:
    """
    Gets a list of paths to files in a specified folder.

    :param fold_path_: A string containing the path to the folder.
    :return: List of paths to files.
    """
    return [os.path.join(fold_path_, file) for file in os.listdir(fold_path_)
            if check_file(os.path.join(fold_path_, file))]


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


def sort_fast(lst_: List[int]) -> List[int]:
    """

    :param lst_:
    :return:
    """
    def _partition(items: List, low: int, high: int) -> int:
        """

        :param items:
        :param low:
        :param high:
        :return:
        """
        pivot, i, j = items[(low + high) // 2], low - 1, high + 1

        while True:
            i += 1
            while items[i] < pivot:
                i += 1

            j -= 1
            while items[j] > pivot:
                j -= 1

            if i >= j:
                return j

            items[i], items[j] = items[j], items[i]

    def _quick_sort(nums: List[int]) -> None:
        """

        :param nums:
        :return:
        """
        def quick_sort(items: List, low: int, high: int) -> None:
            """

            :param items:
            :param low:
            :param high:
            :return:
            """
            if low < high:
                split_index = _partition(items, low, high)
                quick_sort(items, low, split_index)
                quick_sort(items, split_index + 1, high)

        quick_sort(nums, 0, len(nums) - 1)

    _quick_sort(lst_)
    return lst_


def clean_fast(lst_: List[int], count_: int = 0) -> List[int]:
    values = []

    while count_ < len(lst_):
        if (not values or lst_[count_] != values[-1]) and str(lst_[count_]).startswith(NUM_START_WITH):
            values.append(lst_[count_])

        count_ += 1

    return values


def read_file(file_path_: str) -> List[int]:
    """
    Reading a file and getting a list of data.
    :param file_path_: A string containing the path to the file.
    :return: A list with the data retrieved from the file.
    """
    def _read_csv() -> List[int]:
        """
        Reading data from a CSV file.
        :return: A list with the data retrieved from the CSV file.
        """
        with open(file_path_, newline="") as csv_file:
            try:
                return [int(process_row(row)) for row in csv.reader(csv_file, delimiter=",") if check_frmt_row(row)]

            except IndexError:
                pass

    def _read_txt() -> List[int]:
        """
        Reading data from a TXT file.
        :return: A list with the data retrieved from the TXT file.
        """
        with open(file_path_, READ_OPT) as txt_file:
            return [int(process_row(row)) for row in txt_file.readlines() if check_frmt_row(row)]

    def _get_data() -> List:
        """

        :return:
        """
        return _read_csv() if file_path_.endswith(CSV_TYPE) else _read_txt()

    return clean_fast(sort_fast(_get_data())) if check_file(file_path_) else list()


def save_file(file_path_: str, msisdn_lst_: List[str], space_: str, file_type_: str = CSV_TYPE, limit_: int = None,
              first_row_: str = None, file_to_write: IO = None, count_r: int = 1, count_f: int = 1) -> None:
    """

    :param file_path_:
    :param msisdn_lst_:
    :param file_type_:
    :param limit_:
    :param first_row_:
    :param file_to_write:
    :param count_f:
    :param count_r:
    :param space_:
    :return:
    """
    def _open_file(path_: str) -> IO:
        """

        :param path_:
        :return:
        """
        return open(path_, "w") if file_type_ == TXT_TYPE else open(path_, "a", newline="", encoding="utf-8")

    def _change_file_name() -> str:
        """

        :return:
        """
        return file_path_.replace(file_path_[-4:], f"_{count_f}_{space_}{file_type_}")

    def _write_row(msisdn_hash_: Any) -> None:
        """

        :param msisdn_hash_:
        :return:
        """
        if file_type_ == TXT_TYPE:
            file_to_write.write(f"{msisdn_hash_}\n")
        else:
            csv.writer(file_to_write).writerow([msisdn_hash_])

    def _write_first_row() -> None:
        """

        :return:
        """
        if first_row_:
            _write_row(first_row_)

    def _division_into_parts() -> None:
        """

        :return:
        """
        nonlocal file_to_write, count_f

        if (file_to_write is None) or ((limit_ is not None) and (file_to_write.tell() >= limit_)):
            if file_to_write is not None:
                file_to_write.close()
            file_to_write = _open_file(_change_file_name())
            _write_first_row()

            count_f += 1

    while count_r < len(msisdn_lst_):
        _division_into_parts()
        _write_row(msisdn_lst_[count_r])

        count_r += 1

    file_to_write.close()


if __name__ == '__main__':
    pass
