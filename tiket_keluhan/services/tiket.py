from typing import Union, List
from tiket_keluhan.models import (
    TiketModel as _TiketModel
)


def getTiketAsNasabah(login_id) -> Union[None, List[_TiketModel]]:
    tiket_nasabah = _TiketModel.objects.filter(login_id=login_id).all()
    return tiket_nasabah

def getTiketAsOperator(login_id) -> Union[None, List[_TiketModel]]:
    pass

def getTiketAsDirektur(login_id) -> Union[None, List[_TiketModel]]:
    pass

def getTiketAsPikahKetiga(login_id) -> Union[None, List[_TiketModel]]:
    pass

if __name__=="__main__":
    """Do Noting"""
    pass