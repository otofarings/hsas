import base64
import hashlib as hs
from typing import List

from config import BYTEORDER, ENCOD, SALT_ENCOD


def hash_lst(lst_: List[int], count_: int = 0, salt_: str = None) -> List[str]:
    """

    :param lst_:
    :param count_:
    :param salt_:
    :return:
    """
    hash_msisdn_lst = []
    while count_ < len(lst_):
        msisdn = str(lst_[count_])

        if salt_ is None:
            hash_msisdn = hs.md5(bytes(msisdn.strip(), encoding=ENCOD)).hexdigest()
        else:
            hash_msisdn = base64.urlsafe_b64encode(
                hs.md5(salt_.encode(SALT_ENCOD) + bytes(int(msisdn.strip()).to_bytes(8, BYTEORDER))).digest()
            ).decode(SALT_ENCOD)

        hash_msisdn_lst.append(hash_msisdn)
        count_ += 1

    return hash_msisdn_lst
