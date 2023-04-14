import base64
import hashlib as hs
from typing import List


def hash_lst(lst_: List[int], count_: int = 0, salt_: str = None) -> List[str]:
    hash_msisdn_lst = []
    while count_ < len(lst_):
        msisdn = str(lst_[count_])

        if salt_ is None:
            hash_msisdn = hs.md5(bytes(msisdn.strip(), encoding='utf-8')).hexdigest()
        else:
            hash_msisdn = base64.urlsafe_b64encode(
                hs.md5(salt_.encode('ASCII') + bytes(int(msisdn.strip()).to_bytes(8, 'big'))).digest()
            ).decode('ASCII')

        hash_msisdn_lst.append(hash_msisdn)
        count_ += 1

    return hash_msisdn_lst


if __name__ == '__main__':
    pass
