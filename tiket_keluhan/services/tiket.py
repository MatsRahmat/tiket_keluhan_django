from typing import Union, List, Protocol, Optional
from datetime import date
from tiket_keluhan.models import (
    TiketModel as _TiketModel
)

_ListTiket = List[_TiketModel]

def getTiketAsNasabah(login_id) -> Union[None, _ListTiket]:
    tiket_nasabah = _TiketModel.objects.filter(login_id=login_id).all()
    return tiket_nasabah

def getTiketAsOperator(*,
                       end_date: Optional[date]
                       ,start_date: Optional[date]
                       ,login_id: Optional[str]
                       ,tiket_no: Optional[str]
                       ,status: Optional[str]
                       ) -> Union[None, _ListTiket]:
    """
    Get tiket data as operator or direcktur
    """
    
    qr = _TiketModel.objects.all()

    if status:
        qr = qt.filter(status=status)
    
    if end_date and start_date:
        qr = qr.filter(created_at__range=(start_date,end_date))
    
    if login_id:
        qr = qr.filter(login_id=login_id)

    if tiket_no: 
        qr = qr.filter(no_tiket=tiket_no)
    
    
    return qr.order_by('-created_at')

def getTiketAsDirektur(login_id) -> Union[None, _ListTiket]:
    pass

def getTiketAsPikahKetiga(login_id) -> Union[None, _ListTiket]:
    pass

if __name__=="__main__":
    """Do Noting"""
    pass


# Private Class
class _TiketOPProtocol(Protocol):
    
    start_date: Optional[date]
    end_date: Optional[date]
    login_id: Optional[str]
    tiket_no: Optional[str]
    