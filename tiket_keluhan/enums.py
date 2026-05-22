from enum import Enum

class RoleEnum(Enum):
    diretur = 1
    operator = 2
    staff = 3
    pihak_ketiga =4
    nasabah = 6
    
    
class MesgTitleEnum(Enum):
    SUCCESS = "Berhasil"
    FAILED  = "Gagal"
    WARNING = "Peringatan"


class TiketStatusEnum(Enum):
    SENT = "sent"
    APPROVED = "approved"
    ON_PROGRES="on progres"
    DONE    = "done"
    REJECT  = "reject"