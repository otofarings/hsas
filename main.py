from file_processing import get_files_lst_in_dir, read_file, save_file, CSV_TYPE, TXT_TYPE, STABLE_TYPE
from hashing import hash_lst


SALT = "salt"
LIMIT = "limit"
FILE_TYPE = "file_type"
FIRST_ROW = "first_row"

INSURANCE = 500000

SPACES = {
    "YD": {FILE_TYPE: CSV_TYPE, FIRST_ROW: "phone", SALT: None, LIMIT: 1048576000},
    "FB": {FILE_TYPE: TXT_TYPE, FIRST_ROW: None, SALT: None, LIMIT: None},
    "IG": {FILE_TYPE: TXT_TYPE, FIRST_ROW: None, SALT: None, LIMIT: None},
    "VK": {FILE_TYPE: TXT_TYPE, FIRST_ROW: None, SALT: None, LIMIT: 20971520},
    "MT": {FILE_TYPE: TXT_TYPE, FIRST_ROW: None, SALT: None, LIMIT: 134217728},
    "DV360": {FILE_TYPE: CSV_TYPE, FIRST_ROW: "Phone", SALT: None, LIMIT: None},
    "YT": {FILE_TYPE: CSV_TYPE, FIRST_ROW: "Phone", SALT: None, LIMIT: None},
    "AdRiver": {FILE_TYPE: STABLE_TYPE, FIRST_ROW: None, SALT: "pMv=mlB5W98hRK?7YGE+2hGC", LIMIT: None},
    "Buzzoola": {FILE_TYPE: STABLE_TYPE, FIRST_ROW: None, SALT: "kDXCcw-+EosKJ~4Lz+8CUVni", LIMIT: None},
    "OTM": {FILE_TYPE: STABLE_TYPE, FIRST_ROW: None, SALT: "irA%jh@s_g|Z&8Ug_iW@fhLM", LIMIT: None}
}

# Яндекс – hash - .CSV + название столбца "phone"
# Фейсбук/IG – msisdn - .TXT
# ВК – hash - .TXT
# МТ – hash - .TXT
# DV360/youtube - MSI - .CSV + название столбца "Phone"
# TargetRTB - hash - .CSV


def run_script(fold_path_: str, spaces_lst_: list) -> None:
    files_lst = get_files_lst_in_dir(fold_path_)
    while len(files_lst) > 0:
        file_path = files_lst.pop()
        msisdn_lst = read_file(file_path)

        spaces_count = 0
        while spaces_count < len(spaces_lst_):
            space = spaces_lst_[spaces_count]
            msisdn_hash_lst = hash_lst(msisdn_lst, salt_=SPACES[space][SALT])
            save_file(
                file_path_=file_path,
                msisdn_lst_=msisdn_hash_lst,
                space_=space,
                file_type_=SPACES[space][FILE_TYPE],
                limit_=(SPACES[space][LIMIT] - INSURANCE) if SPACES[space][LIMIT] is not None else None,
                first_row_=SPACES[space][FIRST_ROW]
            )

            spaces_count += 1


if __name__ == '__main__':
    try:
        run_script(
            "/Users/mac/data/Hash/to_hash",  # input("Type path to folder: ")
            [sp.strip() for sp in input(f"Type Spaces -> ({', '.join(SPACES.keys())}): ").split(", ")]
        )
    except (KeyboardInterrupt, SystemExit):
        pass
