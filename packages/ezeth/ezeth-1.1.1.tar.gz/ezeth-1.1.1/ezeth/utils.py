from functools import wraps
from pathlib import Path
from eth_account.account import Account
from hexbytes.main import HexBytes
from web3.contract import Contract
from web3.datastructures import AttributeDict
from web3.middleware import geth_poa_middleware
from eth_account.signers.local import LocalAccount
from web3.types import BlockData, BlockIdentifier, TxData, TxReceipt
from web3.logs import DISCARD

def check_connection(f):
    @wraps(f)
    def decorator(self, *args, **kwargs):
        if not self.isConnected:
            raise ConnectionError("Instance is not connected to ethereum node")
        return f(self, *args, **kwargs)
    return decorator