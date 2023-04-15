from config import INPUT_DELIM, FILE_TYPE, FIRST_INPUT, FIRST_ROW, LIMIT, SPACES, SALT, SECOND_INPUT
from process_file import get_files_lst_in_dir, read_file, save_file
from hashing import hash_lst


def run_hashing(fold_path_: str, spaces_lst_: list) -> None:
    """

    :param fold_path_:
    :param spaces_lst_:
    :return:
    """
    files_lst = get_files_lst_in_dir(fold_path_)
    while len(files_lst) > 0:
        file_path = files_lst.pop()
        msisdn_lst = read_file(file_path)

        if msisdn_lst:
            spaces_count = 0
            while spaces_count < len(spaces_lst_):
                space = spaces_lst_[spaces_count]
                msisdn_hash_lst = hash_lst(msisdn_lst, salt_=SPACES[space][SALT])
                save_file(
                    file_path_=file_path,
                    msisdn_lst_=msisdn_hash_lst,
                    space_=space,
                    file_type_=SPACES[space][FILE_TYPE],
                    limit_=SPACES[space][LIMIT] if SPACES[space][LIMIT] is not None else None,
                    first_row_=SPACES[space][FIRST_ROW]
                )

                spaces_count += 1


def start_script() -> None:
    """

    :return:
    """
    try:
        run_hashing(
            input(FIRST_INPUT),
            [sp.strip() for sp in input(SECOND_INPUT).split(INPUT_DELIM)]
        )
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    start_script()
