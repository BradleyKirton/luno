import abc


class LunoClientABC(abc.ABC):
    @abc.abstractproperty
    def _has_auth_details(self) -> bool:
        pass


class LunoClientBase(LunoClientABC):
    PERM_R_BALANCE = 1
    PERM_R_TRANSACTIONS = 2
    PERM_W_SEND = 4
    PERM_R_ADDRESSES = 8
    PERM_W_ADDRESSES = 16
    PERM_R_ORDERS = 32
    PERM_W_ORDERS = 64
    PERM_R_WITHDRAWALS = 128
    PERM_W_WITHDRAWALS = 256
    PERM_R_MERCHANT = 512
    PERM_W_MERCHANT = 1024
    PERM_W_CLIENTDEBIT = 8192
    PERM_W_CLIENTCREDIT = 16384
    PERM_R_BENEFICIARIES = 32768
    PERM_W_BENEFICIARIES = 65536

    BASE_URI = 'https://api.mybitx.com/api/1/'

    @property
    def _has_auth_details(self) -> bool:
        return all([self.api_key is not None, self.secret is not None])