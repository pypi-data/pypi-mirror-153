from web3.exceptions import TransactionNotFound

class UserError(Exception):
    pass

class ContractError(Exception):
    pass

class MethodNotFound(ContractError):
    pass

class EventNotFound(ContractError):
    pass

class ConnectionError(Exception):
    pass