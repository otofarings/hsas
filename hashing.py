import base64
import hashlib as hs
from typing import List

from config import BYTEORDER, ENCOD, SALT_ENCOD


def hash_md5(str_to_hash_: str) -> str:
    """
    Hashing a string.
    :param str_to_hash_: A string to hash.
    :return: A hashed string.
    """
    return hs.md5(bytes(str_to_hash_.strip(), encoding=ENCOD)).hexdigest()


def hash_md5_salt(str_to_hash_: str, salt_: str) -> str:
    """
    Hashing a string with a secret key.
    :param str_to_hash_: A string to hash.
    :param salt_: A secret key to hash the string.
    :return: A hashed string.
    """
    return base64.urlsafe_b64encode(
        hs.md5(salt_.encode(SALT_ENCOD) + bytes(int(str_to_hash_.strip()).to_bytes(8, BYTEORDER))).digest()
    ).decode(SALT_ENCOD)


def choose_hash_method(str_to_hash_: str, salt_: str = None) -> str:
    """
    Choose the method of hashing.
    :param str_to_hash_: A string to hash.
    :param salt_: A secret key to hash the string.
    :return: A hashed string.
    """
    return hash_md5(str_to_hash_) if salt_ is None else hash_md5_salt(str_to_hash_, salt_)


def hash_lst(lst_: List[int], salt_: str = None) -> List[str]:
    """
    Hashing a list of msisdn.
    :param lst_: A list of msisdn.
    :param salt_: A secret key to hash the msisdn.
    :return: A list of hashed msisdn.
    """
    return [choose_hash_method(str(msisdn).strip(), salt_) for msisdn in lst_]
