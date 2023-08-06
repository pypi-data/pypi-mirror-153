"""Constants used for simpleth test cases"""
from simpleth import Blockchain


# Contract used for testing (must match a Solidity file name)
CONTRACT_NAME = 'Test'

# Parameters for CONTRACT_NAME's constructor
CONSTRUCTOR_SENDER = Blockchain().address(0)
CONSTRUCTOR_ARG = 10  # Test constructor expects uint to set `initNum`
CONSTRUCTOR_EVENT_NAME = 'TestConstructed'
CONSTRUCTOR_GAS_LIMIT = 2_000_000    # deploy() currently takes 698,571 gas units

# Parameters for a test transaction in CONTRACT_NAME
#
# TBD - looks like I ought to prepend 'TEST_' to all these
# and move CONTRACT_NAME into this stanza and call it TEST_CONTRACT_NAME, right?
TRX_SENDER = Blockchain().address(0)
TRX_NAME = 'storeNums'
TRX_ARG0 = 50
TRX_ARG1 = 60
TRX_ARG2 = 70
TRX_VALUE = 0       # amount of wei sent with trx. storeNums sends 0
TRX_ARG_KEY1 = '_num0'
EVENT_NAME = 'NumsStored'
EVENT_ARG_KEY1 = 'num0'
EVENT_ARG_VALUE1 = 10

# Parameters for a transaction in a contract that is never deployed
# Used to test creating a contract object and then running a transaction
# without a `connect()` or a `deploy()`. A common mistake when hand-testing
# with the Python interpreter.
NEVER_DEPLOYED_CONTRACT_NAME = 'TestNeverDeployed'
NEVER_DEPLOYED_TRX_SENDER = Blockchain().address(0)
NEVER_DEPLOYED_TRX_NAME = 'setText'

# Parameters for a transaction to test sending a transaction a bad
# `index out-of-bounds` (OOB) arg.
OOB_CONTRACT_NAME = 'Test'
OOB_TRX_SENDER = Blockchain().address(0)
OOB_TRX_NAME = 'storeNum'
OOB_TRX_ARG0 = 100
OOB_TRX_ARG1 = 5

# Parameters for a transaction to test sending a transaction with an arg
# that causes a `divide-by-zero` (DB0) error.
DB0_CONTRACT_NAME = 'Test'
DB0_TRX_SENDER = Blockchain().address(0)
DB0_TRX_NAME = 'divideInitNum'
DB0_TRX_ARG0 = 0

# General constants used for test cases.
HASH_SZ = 66  # number chars in a blockchain hash
GAS_LIMIT_MIN = 21000  # minimum for a trx (https://ethereum.org/en/developers/docs/gas/#what-is-gas-limit)
GAS_LIMIT_MAX = 6721975  # maximum for a trx by Ganache with current default config.
MAX_PRIORITY_FEE_GWEI = 200  # arbitrary value
MAX_FEE_GWEI = 205    # arbitrary value

# Test.sol contract constants
INIT_NUM0 = 0      # nums[0] is initialized to 0
INIT_NUM1 = 1
INIT_NUM2 = 2

# Parameters for a test transaction in CONTRACT_NAME
# This is used to set a variety of types for public state variables.
#
# TBD - should I redo TRX_* (see above) into TRX1_*?
TRX2_SENDER = Blockchain().address(0)
TRX2_NAME = 'storeTypes'
BOOL_VAR_NAME = 'testBool'
BOOL_VAR_VALUE = True
ENUM_VAR_NAME = 'testEnum'
ENUM_VAR_VALUE = 1        # corresponds to MEDIUM Size enum
INT_VAR_NAME = 'testInt'
INT_VAR_VALUE = -123
UINT_VAR_NAME = 'testUint'
UINT_VAR_VALUE = 100
ADDR_VAR_NAME = 'testAddr'
ADDR_VAR_VALUE = Blockchain().address(1)
STR_VAR_NAME = 'testStr'
STR_VAR_VALUE = 'test string'
TEST_ARRAY_VAR_NAME = 'testArray'
TEST_ARRAY_VAR_VALUE = [10, 20, 30]

ARRAY_VAR_NAME = 'nums'
ARRAY_VAR_VALUE = TRX_ARG0     # nums[0] value
