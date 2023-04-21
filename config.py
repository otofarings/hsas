import os

from dotenv import load_dotenv


def convert_megabytes_to_bytes(num_of_mb_: int) -> int:
    """
    Convert megabytes to bytes.
    :param num_of_mb_: A number of megabytes.
    :return: A number of bytes.
    """
    return num_of_mb_ * (1024 * 1024)


load_dotenv()  # Load environment variables from .env file

APPEND_OPT = "a"  # Option to append data to file
READ_OPT = "r"  # Option to read data from file
WRITE_OPT = "w"  # Option to write data to file

ENCOD = "utf-8"  # Encoding used to convert strings to bytes and back
SALT_ENCOD = "ASCII"  # Encoding used to convert salt to bytes and back
BYTEORDER = "big"  # Byte order used to convert integers to bytes and back

DELIM = ","  # Delimiter for csv file
INPUT_DELIM = ", "  # Delimiter for input file
HIDDEN_FILE = "."  # Hidden file

# File extensions
CSV_TYPE = ".csv"
TXT_TYPE = ".txt"
UIDS_TYPE = ".uids"
STABLE_TYPE = ".stable"

# Ad spaces names for witch file creating
AR_SPACE = "AdRiver"
BZ_SPACE = "Buzzoola"
DV_SPACE = "DV360"
FB_SPACE = "Facebook"
IG_SPACE = "Instagram"
MT_SPACE = "MyTarget"
OTM_SPACE = "OTM"
SP_SPACE = "Sape"
VK_SPACE = "VKontakte"
YD_SPACE = "Yandex"
YT_SPACE = "YouTube"
ALL_SPACES = (AR_SPACE, BZ_SPACE, DV_SPACE, FB_SPACE, IG_SPACE, MT_SPACE, OTM_SPACE, VK_SPACE, YD_SPACE, YT_SPACE)

NUM_START_WITH = "7"  # Country code at the beginning of the phone number

SALT = "salt"  # Secret key for hashing
LIMIT = "limit"  # Limit of bytes in file
FILE_TYPE = "file_type"  # File extension
FIRST_ROW = "first_row"  # First row in file

overfill_insurance = convert_megabytes_to_bytes(10)  # 10 MB for insurance of max size of file

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
        LIMIT: convert_megabytes_to_bytes(128) - overfill_insurance
    },
    # OTM: hash md5 with salt + .stable
    OTM_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: STABLE_TYPE,
        SALT: os.getenv(OTM_SPACE.upper()),
        LIMIT: None
    },
    # Sape: hash md5 with salt + .stable
    SP_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: STABLE_TYPE,
        SALT: os.getenv(SP_SPACE.upper()),
        LIMIT: None
    },
    # VKontakte: hash + .txt (min 2000, max 5000000)
    VK_SPACE: {
        FIRST_ROW: None,
        FILE_TYPE: TXT_TYPE,
        SALT: None,
        LIMIT: convert_megabytes_to_bytes(128) - overfill_insurance
    },
    # Yandex: "phone" + hash md5 + .csv (min 100, max ...)
    YD_SPACE: {
        FIRST_ROW: "phone",
        FILE_TYPE: CSV_TYPE,
        SALT: None,
        LIMIT: convert_megabytes_to_bytes(1000) - overfill_insurance
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
