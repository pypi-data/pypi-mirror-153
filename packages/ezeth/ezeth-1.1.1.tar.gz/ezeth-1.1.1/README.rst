Simple Ethereum Client
======================

This repository is a python client to access ethereum network.

Requirements
------------

-  `Web3.py <https://web3py.readthedocs.io/en/stable/index.html>`__
-  `py-solc-x <https://solcx.readthedocs.io/en/latest/>`__

Usage
-----

-  `Instantiate client <#instantiate-client>`__
-  `Check connection <#check-connection>`__
-  `Connect to new node <#connect-to-new-node>`__
-  `Create new ethereum account <#create-new-ethereum-account>`__
-  `Get account instance <#get-account-instance>`__
-  `Get account properties <#get-account-properties>`__
-  `Change account password <#change-account-password>`__
-  `Transfer balance to another
   account <#transfer-balance-to-another-account>`__
-  `Compile smart contract <#compile-smart-contract>`__
-  `Deploy smart contract <#deploy-smart-contract>`__
-  `Get contract <#get-contract>`__
-  `Modify contract's storage <#modify-contracts-storage>`__
-  `Parse contract event log <#parse-contract-event-log>`__
-  `Call contract <#call-contract>`__
-  `Cancel transaction <#cancel-transaction>`__
-  `Get blockchain data <#get-blockchain-data>`__

Instantiate client
~~~~~~~~~~~~~~~~~~

Initialize the client

.. code:: python

   from ezeth import ETHClient

   node_host = 'localhost'
   node_port = 8545
   node_connection_type = 'http'
   node_consensus = 'PoW'

   client = ETHClient(
       node_host=node_host,
       node_port=node_port,
       node_connection_type=node_connection_type,
       node_consensus=node_consensus
   )

Check connection
~~~~~~~~~~~~~~~~

.. code:: python

   print(client.isConnected)
   # True

Connect to new node
~~~~~~~~~~~~~~~~~~~

.. code:: python

   node_host = 'localhost'
   node_port = 8546
   node_connection_type = 'http'
   node_consensus = 'PoW'

   client.connect(
       node_host=node_host,
       node_port=node_port,
       node_connection_type=node_connection_type,
       node_consensus=node_consensus
   )

Create new ethereum account
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The returned object is dictionary with 2 keys,

-  ``"account"``, contains the instance of ``LocalAccount``
-  ``"encrypted_key"``, contains the dictionary that contains address
   and private key of the account encrypted with password input from the
   parameter

.. code:: python

   import json
   from eth_account.signers.local import LocalAccount

   password = 'pass123'

   new_account = client.create_account(password)

   print(isinstance(new_account, LocalAccount))
   # True

   with open('account_data.json', 'w') as f:
       json.dump(new_account['encrypted_key'], f)

Get account instance
~~~~~~~~~~~~~~~~~~~~

To get account instance from encrypted private key, use this method

.. code:: python

   import json
   from eth_account.signers.local import LocalAccount

   password = 'pass123'

   with open('account_data.json') as f:
       encrypted_key = json.load(f)

   account = client.get_account(
       password,
       encrypted_key
   )

   print(isinstance(account, LocalAccount))
   # True

To get account instance from private key, use this method

.. code:: python

   # don't use this private key in development
   private_key = '0xd69ff3bd9e6a4455c13974be6ac741996c94eedf9725ad3c7fbccb833d3fae79'

   account = client.get_account_from_key(private_key)

   print(isinstance(account, LocalAccount))
   # True

Get account properties
~~~~~~~~~~~~~~~~~~~~~~

The returned object is dictionary with 3 keys,

-  ``"address"``, the address of the account
-  ``"balance"``, the balance of the account at current network
-  ``"nonce"``, the current nonce (number of transactions) of the
   account at current network

.. code:: python

   account_address = account.address

   account_properties = client.get_account_properties(account_address)

   print(account_properties)
   # {'address': '0xf3cCa25419069bcd6B94bE3876Ac3400070E4796', 'balance': 0, 'nonce': 0}

Change account password
~~~~~~~~~~~~~~~~~~~~~~~

To change password of the encrypted private key, use this method

.. code:: python

   import json

   old_password = 'pass123'
   new_password = 'newpasss123'

   with open('account_data.json') as f:
       encrypted_key = json.load(f)

   new_encrypted_key = client.change_account_password(
       old_password,
       new_password,
       encrypted_key
   )

   with open('new_account_data.json', 'w') as f:
       json.dump(new_encrypted_key, f)

Transfer balance to another account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   receiver_address = '0xf3cCa25419069bcd6B94bE3876Ac3400070E4796'
   value = 10
   message = 'here is the money'

   transaction = client.transfer(
       receiver_address,
       value,
       message,
       account=account
   )

To estimate the cost to transfer, use this

.. code:: python

   cost = client.estimate_transfer_price(
       value,
       message
   )

   print(cost)
   # {'cost': 664680000000000, 'value': 10, 'total': 664680000000010}

Compile smart contract
~~~~~~~~~~~~~~~~~~~~~~

The returned object is dictionary with keys in format
``<filename>:<contractname>`` (ex. ``"Storage.sol:Storage"``) and the
value is dictionary with 2 keys,

-  ``"abi"``, contains ABI of the contract
-  ``"bin"``, contains bytecode of the contract

.. code:: python

   solc_version = '0.8.11'
   sol_file = 'Storage.sol'

   compiled_contract = client.compile_contract(
       sol_file,
       solc_version
   )

Here is example of contract

.. code:: solidity

   // SPDX-License-Identifier: GPL-3.0

   // Storage.sol

   pragma solidity >=0.4.16 <0.9.0;

   contract Storage {
       uint storedData;

       event ValueModified(
           uint oldValue,
           uint newValue
       );

       constructor(uint initValue) {
           storedData = initValue;
       }

       function set(uint newValue) public {
           emit ValueModified(storedData, newValue);
           storedData = newValue;
       }

       function get() public view returns (uint) {
           return storedData;
       }
   }

Deploy smart contract
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   storage_contract = compiled_contract['Storage.sol:Storage']
   contract_bytecode = storage_contract['bin']
   contract_abi = storage_contract['abi']

   # for contract constructor
   init_value = 10

   deployed_contract_data = client.deploy_contract(
       contract_bytecode,
       contract_abi,
       account=account,
       initValue=init_value
   )

To estimate the cost to deploy smart contract, use this

.. code:: python

   cost = client.estimate_deploy_contract_price(
       contract_bytecode,
       contract_abi,
       account_address=account.address,
       initValue=init_value
   )

   print(cost)
   # {'cost': 5166480000000000, 'value': 0, 'total': 5166480000000000}

..

   The account which deployed the smart contract must have a sufficient
   balance to estimate the cost if the constructor is payable method.

Get contract
~~~~~~~~~~~~

To get the deployed smart contract address, use this

.. code:: python

   transaction_hash = deployed_contract_data['transaction_hash']

   contract_address = client.get_contract_address(transaction_hash)

   print(contract_address)
   # 0x7c0ce101E6712DD4E447CE2af81AAD5f8fbF34D0

To get the instance of the deployed smart contract, use this

.. code:: python

   contract = client.get_contract(
       contract_address,
       contract_abi
   )

Modify contract's storage
~~~~~~~~~~~~~~~~~~~~~~~~~

To modify contract storage by contract method, use this

.. code:: python

   contract_method = 'set'
   new_value = 13

   transaction = client.contract_method(
       contract_method,
       contract=contract,
       account=account,
       newValue=new_value
   )

To test contract method locally without sending transaction to network, use this

.. code:: python

   # will raise exception if something wrong, else return True
   client.contract_method_test(
      contract_method,
      contract=contract,
      account_address=account.address,
      newValue=new_value
   )

To estimate the cost, use this

.. code:: python

   cost = client.estimate_contract_method_price(
       contract_method,
       contract=contract,
       account_address=account.address,
       newValue=new_value
   )

   print(cost)
   # {'cost': 811560000000000, 'value': 0, 'total': 811560000000000}

..

   The account which modify the smart contract's storage must have a
   sufficient balance to estimate the cost if the method is payable
   method.

Parse contract event log
~~~~~~~~~~~~~~~~~~~~~~~~

To parse event log that is emitted from modified smart contract, use
this

.. code:: python

   event_name = 'ValueModified'
   transaction_hash = transaction['hash']

   event_log = client.parse_contract_event_log(
       event_name,
       transaction_hash,
       contract=contract
   )

Call contract
~~~~~~~~~~~~~

To call contract's ``pure`` and ``view`` methods, use this

.. code:: python

   contract_method = 'get'

   currentValue = client.contract_call(
       contract_method,
       contract=contract
   )

   print(currentValue)
   # 13

Cancel transaction
~~~~~~~~~~~~~~~~~~

To cancel any transaction from account, use this

.. code:: python

   transaction_hash = transaction['hash']

   new_transaction = client.cancel_transaction(
       transaction_hash,
       account=account
   )

To estimate the cost, use this

.. code:: python

   cost = client.estimate_cancel_transaction_price(
       transaction_hash
   )

   print(cost)
   # {'cost': 811590000000000, 'value': 0, 'total': 811590000000000}

..

   Transaction that already verified or mined can't be canceled. The way
   the transaction canceled is by sending new empty transaction with the
   same nonce but higher gas price so the empty transaction will be
   mined and the old one will be discarded.

Get blockchain data
~~~~~~~~~~~~~~~~~~~

To get detailed transaction from transaction hash, use this

.. code:: python

   transaction = client.get_transaction(transaction_hash)

To get transaction receipt (the prove that transaction is verified or
mined), use this

.. code:: python

   receipt = client.get_transaction_receipt(transaction_hash)

To get detailed block, use this

.. code:: python

   block = client.get_block('latest')
