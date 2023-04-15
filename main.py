from typing import List, Tuple

from config import INPUT_DELIM, FILE_TYPE, FIRST_INPUT, FIRST_ROW, LIMIT, SPACES, SALT, SECOND_INPUT
from process_file import get_files_lst_in_dir, get_lst_of_msisdn, save_file
from hashing import hash_lst


def hash_and_process_file(file_path_: str, msisdn_lst_: List[int], space_: str) -> None:
    """
    Hashing a list of msisdn and save it to a file.
    :param file_path_: A path to file.
    :param msisdn_lst_: A list of bytes.
    :param space_: A space.
    :return:
    """
    save_file(
        file_path_=file_path_,
        msisdn_lst_=hash_lst(msisdn_lst_, salt_=SPACES[space_][SALT]),
        space_=space_,
        file_type_=SPACES[space_][FILE_TYPE],
        limit_=SPACES[space_][LIMIT],
        first_row_=SPACES[space_][FIRST_ROW]
    )


def hash_by_iter_space(file_path_: str, msisdn_lst_: List[int], spaces_lst_: List[str]) -> None:
    """
    Hashing a list of msisdn by iteration spaces.
    :param file_path_: A path to file.
    :param msisdn_lst_: A list of msisdn.
    :param spaces_lst_: A list of spaces.
    :return:
    """
    count_s = 0
    while count_s < len(spaces_lst_):
        space = spaces_lst_[count_s]
        hash_and_process_file(file_path_, msisdn_lst_, space)

        count_s += 1


def iter_and_process_file(paths_of_files_lst_: List[str], spaces_lst_: List[str]) -> None:
    """
    Run hashing function.
    :param paths_of_files_lst_: A list of paths to files.
    :param spaces_lst_: A list of spaces.
    :return:
    """
    count_f = 0
    while count_f < len(paths_of_files_lst_):
        file_path = paths_of_files_lst_[count_f]
        msisdn_lst = get_lst_of_msisdn(file_path)
        if msisdn_lst:
            hash_by_iter_space(file_path, msisdn_lst, spaces_lst_)

        count_f += 1


def get_input() -> Tuple[List[str], List[str]]:
    """
    Get input from user.
    :return: A list of paths to files and a list of spaces.
    """
    def _get_first_input() -> List[str]:
        """
        Get first input from user.
        :return: A list of paths to files.
        """
        fold_path = input(FIRST_INPUT)
        return get_files_lst_in_dir(fold_path)

    def _get_second_input() -> List[str]:
        """
        Get second input from user.
        :return: A list of spaces.
        """
        spaces = input(SECOND_INPUT)
        return spaces.split(INPUT_DELIM)

    return _get_first_input(), _get_second_input()


def start_script() -> None:
    """
    Start script. Get input from user and run hashing function.
    :return:
    """
    try:
        paths_of_files_lst, spaces_lst = get_input()
        if paths_of_files_lst and spaces_lst:
            iter_and_process_file(paths_of_files_lst, spaces_lst)

    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    start_script()
