import csv
import os
from typing import List, Any, IO, Iterable

from config import TXT_TYPE, CSV_TYPE, READ_OPT, WRITE_OPT, APPEND_OPT, NUM_START_WITH, DELIM, ENCOD, HIDDEN_FILE
from process_row import check_frmt_row, process_row


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
    Delete a file from the system.
    :param file_path_: A string containing the path to the file.
    :return:
    """
    if os.path.exists(file_path_):
        os.remove(file_path_)


def check_file(fold_path_: str, file_path_: str) -> bool:
    """
    Check the file configurations to see if it can be processed.
    Basic conditions:
    - The folder exists in the system;
    - The file is in the folder;
    - The file exists in the system;
    - The file does not start with a dot;
    - The file extension is on the list of files available for processing.
    :param fold_path_: A string containing the path to the folder.
    :param file_path_: A string containing name of the file.
    :return: True if the file has suitable configurations, otherwise False.
    """
    if os.path.isdir(fold_path_):
        if os.path.exists(os.path.join(fold_path_, file_path_)):
            return file_path_.endswith((TXT_TYPE, CSV_TYPE)) and not file_path_.startswith(HIDDEN_FILE)
    return False


def get_files_lst_in_dir(fold_path_: str) -> List[str]:
    """
    Gets a list of paths to files in a specified folder.
    :param fold_path_: A string containing the path to the folder.
    :return: List of paths to files.
    """
    return [os.path.join(fold_path_, file) for file in os.listdir(fold_path_) if check_file(fold_path_, file)]


def sort_fast(lst_: List[int]) -> List[int]:
    """
    Sorts a list of integers using the quick sort algorithm.
    :param lst_: A list of integers.
    :return: A sorted list of integers.
    """
    def _partition(items: List, low: int, high: int) -> int:
        """
        Partitioning a list of integers.
        :param items: A list of integers.
        :param low: A number indicating the start of the list.
        :param high: A number indicating the end of the list.
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
        Quick sort algorithm.
        :param nums: A list of integers.
        :return:
        """
        def quick_sort(items: List, low: int, high: int) -> None:
            """
            Quick sort algorithm.
            :param items: A list of integers.
            :param low: A number indicating the start of the list.
            :param high: A number indicating the end of the list.
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
    """
    Cleaning a list of integers.
    :param lst_: A list of integers.
    :param count_: A number indicating the start of the list.
    """
    values = []

    while count_ < len(lst_):
        if (not values or lst_[count_] != values[-1]) and str(lst_[count_]).startswith(NUM_START_WITH):
            values.append(lst_[count_])

        count_ += 1

    return values


def get_lst_of_msisdn(file_path_: str) -> List[int] | None:
    """
    Reading a file and getting a list of data.
    :param file_path_: A string containing the path to the file.
    :return: A list of data.
    """
    def _read_file(file_: IO) -> List[str] | List[List[str]]:
        """
        Reading a file.
        :return: A list with the data retrieved from the file.
        """
        def read_csv() -> Iterable[List[str]]:
            """
            Reading a csv file.
            :return: A list with the data retrieved from the file.
            """
            return csv.reader(file_, delimiter=DELIM)

        def read_txt() -> List[str]:
            """
            Reading a txt file.
            :return: A list with the data retrieved from the file.
            """
            return file_.readlines()

        return read_csv() if file_path_.endswith(CSV_TYPE) else read_txt()

    def _open_file() -> IO:
        """
        Opening a file.
        :return: A list with the data retrieved from the file.
        """
        def open_csv() -> IO:
            """
            Opening a csv file.
            :return: A file object.
            """
            return open(file_path_, newline="")

        def open_txt() -> IO:
            """
            Opening a txt file.
            :return: A file object.
            """
            return open(file_path_, READ_OPT)

        return open_csv() if file_path_.endswith(CSV_TYPE) else open_txt()

    def _create_lst_of_msisdn() -> List[int]:
        """
        Creating a list of MSISDN.
        :return: A list with msisdn retrieved from the file.
        """
        with _open_file() as file:
            return [int(process_row(row)) for row in _read_file(file) if check_frmt_row(row)]

    lst_of_msisdn = _create_lst_of_msisdn()
    if lst_of_msisdn:
        return clean_fast(sort_fast(lst_of_msisdn))
    else:
        return None


def save_file(file_path_: str, msisdn_lst_: List[str], space_: str, file_type_: str = CSV_TYPE, limit_: int = None,
              first_row_: str = None, file_to_write: IO = None, count_r: int = 1, count_f: int = 1) -> None:
    """
    Save data to file.
    :param file_path_: Path to file.
    :param msisdn_lst_: List of msisdn.
    :param file_type_: File extension.
    :param limit_: Limit of bytes in file.
    :param first_row_: First row in file.
    :param file_to_write: File to write.
    :param count_f: Count of files.
    :param count_r: Count of rows.
    :param space_: Ad space for witch file creating.
    :return:
    """
    def _open_file(path_: str) -> IO:
        """
        Open file.
        :param path_: Path to file.
        :return: File.
        """
        return open(path_, WRITE_OPT) if file_type_ == TXT_TYPE else open(path_, APPEND_OPT, newline="", encoding=ENCOD)

    def _change_file_name() -> str:
        """
        Change file name.
        :return: New file name.
        """
        return file_path_.replace(file_path_[-4:], f"_{count_f}_{space_}{file_type_}")

    def _write_row(msisdn_hash_: Any) -> None:
        """
        Write row in file.
        :param msisdn_hash_: Row to write.
        :return:
        """
        if file_type_ == TXT_TYPE:
            file_to_write.write(f"{msisdn_hash_}\n")
        else:
            csv.writer(file_to_write).writerow([msisdn_hash_])

    def _write_first_row() -> None:
        """
        Write first row in file.
        :return:
        """
        if first_row_:
            _write_row(first_row_)

    def check_limit() -> bool:
        """
        Check limit of bytes in file.
        :return: True if limit is reached.
        """
        return (limit_ is not None) and (file_to_write.tell() >= limit_)

    def _division_into_parts() -> None:
        """
        Division into parts.
        :return:
        """
        nonlocal file_to_write, count_f

        if (file_to_write is None) or check_limit():
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
