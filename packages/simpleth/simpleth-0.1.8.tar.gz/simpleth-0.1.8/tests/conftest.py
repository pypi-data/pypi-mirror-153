"""conftest.py for simpleth class test cases"""
import pytest

from simpleth import Contract, Results
import testconstants as constants


@pytest.fixture(scope='class')
def construct_test_contract():
    """Set up a simpleth contract object. Return contract object ready for either
    connect() or deploy()"""
    return Contract(constants.CONTRACT_NAME)


@pytest.fixture(scope='class')
def construct_never_deployed_test_contract():
    """Set up a simpleth contract object. Return contract object. Do not deploy.

    There are a set of test cases that expect to use a contract which was compiled
    but never had a `deploy()`. They are testing the exception handling when a transaction
    is run without a `connect()` being done.

    In other words, the `.abi` and `.bin` artifact files exist but there is no
    `.addr` file.

    If this contract is accidentally deployed, just delete the `.addr` file in
    the `artifact` directory.

    """
    return Contract(constants.NEVER_DEPLOYED_CONTRACT_NAME)


@pytest.fixture(scope='class')
def deploy_test_contract(construct_test_contract):
    """Deploy the test contract. Return contract_obj ready to be used for
    transactions."""
    contract_obj = construct_test_contract
    contract_obj.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG)
    return contract_obj


# Should this be (scope='fixture')?
@pytest.fixture(scope='class')
def connect_to_test_contract(construct_test_contract):
    """Connect to previously deployed contract. Return contract_obj ready to
    be used for transactions."""
    contract_obj = construct_test_contract
    contract_obj.connect()
    return contract_obj


@pytest.fixture(scope='class')
def run_test_trx_to_store_nums(connect_to_test_contract):
    """Return simpleth Results object with outcomes from running
    `store_nums()`"""
    contract_obj = connect_to_test_contract
    trx_receipt = contract_obj.run_trx(
        constants.TRX_SENDER,
        constants.TRX_NAME,
        constants.TRX_ARG0,
        constants.TRX_ARG1,
        constants.TRX_ARG2
        )
    results = Results(contract_obj, trx_receipt)
    return results


@pytest.fixture(scope='class')
def run_test_trx_to_store_nums_again(connect_to_test_contract):
    """Use when a test case does two `store_nums()`."""

    # pytest does not let you call the same fixture twice in a test
    # case. For some test cases (see test_get_old_events_two() as an
    # example), store_nums() trx is called twice. Use this fixture
    # for the second call.  (A later comment, I think it is because the first
    # run_test_trx_to_store_nums() creates its contract_obj and this function
    # creates a different contract object. I'm not going to try to investigate
    # and fix. Tests are working.)
    contract_obj = connect_to_test_contract
    trx_receipt = contract_obj.run_trx(
        constants.TRX_SENDER,
        constants.TRX_NAME,
        constants.TRX_ARG0+10,
        constants.TRX_ARG1+10,
        constants.TRX_ARG2+10
        )
    results = Results(contract_obj, trx_receipt)
    return results


@pytest.fixture(scope='class')
def run_test_trx_to_store_array(connect_to_test_contract):
    """Run `store_nums()`. Makes an array in the contract
    ready for testing. Return the contract object."""
    contract_obj = connect_to_test_contract
    contract_obj.run_trx(
        constants.TRX_SENDER,
        constants.TRX_NAME,
        constants.TRX_ARG0,
        constants.TRX_ARG1,
        constants.TRX_ARG2
        )
    return contract_obj


@pytest.fixture(scope='class')
def run_test_trx_to_store_all_types(connect_to_test_contract):
    """Run `store_types()`. Stores various types into the
    contract. Return the contract object."""
    contract_obj = connect_to_test_contract
    contract_obj.run_trx(
        constants.TRX2_SENDER,
        constants.TRX2_NAME,
        constants.BOOL_VAR_VALUE,
        constants.ENUM_VAR_VALUE,
        constants.UINT_VAR_VALUE,
        constants.INT_VAR_VALUE,
        constants.ADDR_VAR_VALUE,
        constants.STR_VAR_VALUE,
        constants.TEST_ARRAY_VAR_VALUE
        )
    return contract_obj
