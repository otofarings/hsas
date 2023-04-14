import os

from dotenv import load_dotenv


def convert_megabytes_to_bytes(num_of_mb_: int) -> int:
    return num_of_mb_ * (1024 * 1024)


load_dotenv()

APPEND_OPT = "a"
READ_OPT = "r"
WRITE_OPT = "w"

ENCOD = "utf-8"
SALT_ENCOD = "ASCII"
BYTEORDER = "big"

DELIM = ","
INPUT_DELIM = ", "
HIDDEN_FILE = "."

CSV_TYPE = ".csv"
TXT_TYPE = ".txt"
UIDS_TYPE = ".uids"
STABLE_TYPE = ".stable"

AR_SPACE = "AdRiver"
BZ_SPACE = "Buzzoola"
DV_SPACE = "DV360"
FB_SPACE = "Facebook"
IG_SPACE = "Instagram"
MT_SPACE = "MyTarget"
OTM_SPACE = "OTM"
VK_SPACE = "VKontakte"
YD_SPACE = "Yandex"
YT_SPACE = "YouTube"
ALL_SPACES = (AR_SPACE, BZ_SPACE, DV_SPACE, FB_SPACE, IG_SPACE, MT_SPACE, OTM_SPACE, VK_SPACE, YD_SPACE, YT_SPACE)

NUM_START_WITH = "7"  # Country code at the beginning of the phone number

SALT = "salt"
LIMIT = "limit"
FILE_TYPE = "file_type"
FIRST_ROW = "first_row"

SPACES = {
    # AdRiver: hash md5 with salt + .stable
    AR_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: STABLE_TYPE,
        SALT: os.getenv(AR_SPACE.upper()),
        LIMIT: None
    },
    # Buzzoola: hash md5 with salt + .stable
    BZ_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: STABLE_TYPE,
        SALT: os.getenv(BZ_SPACE.upper()),
        LIMIT: None
    },
    # DV360: "Phone" + msisdn + .csv
    DV_SPACE: {
        FIRST_ROW: "Phone",
        FILE_TYPE: CSV_TYPE,
        SALT: None,
        LIMIT: None
    },
    # Facebook: msisdn + .txt
    FB_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: TXT_TYPE,
        SALT: None,
        LIMIT: None
    },
    # Instagram: msisdn + .txt
    IG_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: TXT_TYPE,
        SALT: None,
        LIMIT: None
    },
    # MyTarget: hash + .txt (min 2000, max 5000000)
    MT_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: TXT_TYPE,
        SALT: None,
        LIMIT: convert_megabytes_to_bytes(128)
    },
    # OTM: hash md5 with salt + .stable
    OTM_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: STABLE_TYPE,
        SALT: os.getenv(OTM_SPACE.upper()),
        LIMIT: None
    },
    # VKontakte: hash + .txt (min 2000, max 5000000)
    VK_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: TXT_TYPE,
        SALT: None,
        LIMIT: convert_megabytes_to_bytes(128)
    },
    # Yandex: "phone" + hash md5 + .csv (min 100, max ...)
    YD_SPACE: {
        FIRST_ROW: "phone",
        FILE_TYPE: CSV_TYPE,
        SALT: None,
        LIMIT: convert_megabytes_to_bytes(1000)
    },
    # YouTube: "Phone" + msisdn + .csv
    YT_SPACE: {
        FIRST_ROW: "Phone",
        FILE_TYPE: CSV_TYPE,
        SALT: None,
        LIMIT: None
    }
}

FIRST_INPUT = "Type path to folder: "
SECOND_INPUT = f"Type Spaces -> ({INPUT_DELIM.join(SPACES.keys())}): "
