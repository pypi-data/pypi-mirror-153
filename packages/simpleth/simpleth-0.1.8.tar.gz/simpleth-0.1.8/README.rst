``Simpleth`` (**Simplified Ethereum**) simplifies
the use of Python to interact with a Ganache Ethereum blockchain and its Solidity
smart contracts.

`Simpleth` is a set of five Python facade classes that use the ``web3.py`` API
to interact with the smart contracts through a Ganache Ethereum client.

`Simpleth` only supports a portion of the `web3.py` functionality - the
portion that a Python developer uses to interact with contracts.

The aim is to provide Python developers a quick and easy way to:

-  **deploy** contracts onto the blockchain
-  **run transactions** in those contracts
-  **call functions** in those contracts
-  **get values** for public state variables in those contracts
-  **use filters** to find events emitted by those contracts
-  **get data** about the blockchain, contracts, transactions, and events

The intended audience:

-  **Python developers** who want to:

   -  learn to code smart contracts in Solidity
   -  play around with Ethereum and smart contracts using the Python interpreter
      and scripts
   -  build proof-of-concept dapps with Python scripts or `flask`
   -  build production dapps using Python in a single-user test environment
   -  see a working example of the `web3.py` API by looking at `simpleth`
      internals

-  **Solidity developers** looking for examples of:

   -  basic functions in a smart contract, esp. if just starting out
   -  more advanced functions in a smart contract, esp. for use in
      medium-complexity dapps.

**Full documentation** at *Read the Docs*: https://simpleth.readthedocs.io/en/latest/