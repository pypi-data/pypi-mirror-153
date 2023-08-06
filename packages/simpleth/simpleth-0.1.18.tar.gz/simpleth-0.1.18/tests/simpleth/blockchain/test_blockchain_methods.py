"""Test Blockchain() methods"""
import pytest
import re
from simpleth import Contract, Blockchain, SimplEthError


class TestBlockchainMethodsGood:
    """Test cases for Blockchain() methods with good data"""

    def test_address(self):
        """address() returns a valid address for an account number"""
        # check this first. It is used in subsequent tests.
        addr4 = Blockchain().address(4)
        assert(Blockchain().is_valid_address(addr4))

    def test_account_num(self):
        """account_num() returns the correct account number for an address"""
        addr7 = Blockchain().address(7)
        assert(Blockchain().account_num(addr7) == 7)

    def test_balance(self):
        """balance() returns an integer for an address"""
        addr3 = Blockchain().address(3)
        assert(isinstance(Blockchain().balance(addr3), int))

    def test_block_time_epoch(self):
        """block_time_epoch() returns an integer for epoch seconds"""
        # Use last block in chain
        block_num = Blockchain().block_number
        assert(isinstance(Blockchain().block_time_epoch(block_num), int))

    def test_block_time_string_default_format(self):
        """block_time_string() returns the default formatted time string"""
        # Use last block in chain
        block_num = Blockchain().block_number
        # Assumes default time_format is YYYY-MM-DD HH:MM:SS
        default_time_format = \
            "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}"
        assert(
            re.match(
                default_time_format,
                Blockchain().block_time_string(block_num)
                )
            )

    def test_block_time_string_with_time_format(self):
        """block_time_string() returns a specified formatted time string"""
        # Use last block in chain
        block_num = Blockchain().block_number
        # Get simple format, HH:MM
        time_format = "[0-9]{2}:[0-9]{2}"
        assert(
            re.match(
                time_format,
                Blockchain().block_time_string(block_num, '%I:%M')
                )
            )

    @staticmethod
    def fee_history_placeholder():
        """Placeholder for fee_history() test cases"""
        # Ganache has yet to implement the w3.eth_fee_history()
        # method. If and when it is implemented, put in the set of
        # test cases here.  For now, just return a Pass.
        assert True

    def test_is_valid_address_returns_true(self):
        """is_valid_address() returns true for a valid address"""
        addr3 = Blockchain().address(3)
        assert (isinstance(Blockchain().balance(addr3), int))

    def test_send_ether(self):
        """send_ether() transfers Ether from one account to another"""
        user6 = Blockchain().address(6)
        user7 = Blockchain().address(7)
        start_bal6 = Blockchain().balance(user6)
        start_bal7 = Blockchain().balance(user7)
        amount = 2_000_000_000  # wei
        Blockchain().send_ether(user6, user7, amount)
        end_bal6 = Blockchain().balance(user6)
        end_bal7 = Blockchain().balance(user7)
        # user6's end bal = start_bal6 - amount - cost of send_ether() trx
        # The amount and cost of gas is not computed here. Just check
        # that user6's end balance is less than
        assert (
            (end_bal6 < (start_bal6 - amount)) and
            (end_bal7 == (start_bal7 + amount))
            )

    def test_send_ether_to_contract(self):
        """send_ether() transfers Ether from one account to a payable contract"""
        user6 = Blockchain().address(6)
        contract = Contract('test')
        contract.deploy(user6, 10)   # has a fallback receive() function
        start_bal = Blockchain().balance(contract.address)
        amount = 2_000  # wei
        Blockchain().send_ether(user6, contract.address, amount)
        end_bal = Blockchain().balance(contract.address)
        change_in_balance = end_bal - start_bal
        assert change_in_balance == amount

    def test_transaction(self):
        """transaction() returns a string for the transaction result"""
        # Use the valid send_ether test to create a trx hash
        user6 = Blockchain().address(6)
        user7 = Blockchain().address(7)
        amount = 2_000_000_000  # wei
        trx_hash = Blockchain().send_ether(user6, user7, amount)
        assert Blockchain().transaction(trx_hash)['value'] == amount

    def test_trx_count(self):
        """trx_count() returns number of transactions"""
        # Use the valid send_ether test to create at least on trx for user6
        user6 = Blockchain().address(6)
        user7 = Blockchain().address(7)
        amount = 2_000_000_000  # wei
        Blockchain().send_ether(user6, user7, amount)
        num_trx = Blockchain().trx_count(user6)
        assert (isinstance(num_trx, int) and (num_trx > 0))

    def test_trx_sender(self):
        """trx_sender() returns an account address"""
        # Use the valid send_ether test to create a trx hash
        user6 = Blockchain().address(6)
        user7 = Blockchain().address(7)
        amount = 2_000_000_000  # wei
        trx_hash = Blockchain().send_ether(user6, user7, amount)
        assert Blockchain().trx_sender(trx_hash) == user6


class TestBlockchainMethodsBad:
    """Test cases for Blockchain() methods with bad data"""

    @pytest.mark.parametrize('bad_acct_num',
                             [-1, len(Blockchain().accounts), 'xxx']
                             )
    def test_address_raises_b_020_010(self, bad_acct_num):
        """address() with bad account_num raises SimplEthError"""
        with pytest.raises(SimplEthError) as excp:
            Blockchain().address(bad_acct_num)
        assert excp.value.code == 'B-020-010'

    def test_account_num_bad_addr(self):
        """account_num() returns None for invalid account_address"""
        bad_addr = '0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6'
        assert(Blockchain().account_num(bad_addr) is None)

    def test_account_num_bad_type(self):
        """account_num() returns None for bad account_address type"""
        bad_type = 200
        assert(Blockchain().account_num(bad_type) is None)

    def test_balance_with_missing_addr_raises_type_error(self):
        """Test balance() with missing address."""
        with pytest.raises(TypeError):
            Blockchain().balance()

    def test_balance_bad_address_type_raises_b_030_010(self):
        """balance() with bad address type raises SimplEthError"""
        bad_addr_type = 200
        with pytest.raises(SimplEthError) as excp:
            Blockchain().balance(bad_addr_type)
        assert excp.value.code == 'B-030-010'

    def test_balance_bad_address_raises_b_030_020(self):
        """balance() with bad address raises SimplEthError"""
        bad_addr = '0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6'
        with pytest.raises(SimplEthError) as excp:
            Blockchain().balance(bad_addr)
        assert excp.value.code == 'B-030-020'

    @pytest.mark.parametrize('bad_block_num',
                             [-1, Blockchain().block_number + 100, 'xxx']
                             )
    # parametrize gets values at pytest collection time. This test
    # will use a bad_block_num greater than the last block number
    # in the chain. Previous tests increase the block_number. Need
    # to add a number that gives an invalid block number. (If you
    # use 1, you are adding to the block_number when the test starts
    # and by the time it gets to this test case the block_number has
    # increased by 4.)
    def test_block_time_epoch_bad_block_num_raises_b_040_010(
            self,
            bad_block_num
            ):
        print(Blockchain().block_number)
        print(bad_block_num)
        """block_time_epoch() with bad block_num raises SimplEthError"""
        with pytest.raises(SimplEthError) as excp:
            Blockchain().block_time_epoch(bad_block_num)
        assert excp.value.code == 'B-040-010'

    def test_block_time_with_bad_block_number_raises_b_050_010(self):
        """block_time_string() with bad block_number type raises SimplEthError"""
        block_num = Blockchain().block_number + 10
        time_format_string = "%M"
        with pytest.raises(SimplEthError) as excp:
            Blockchain().block_time_string(
                block_num,
                time_format_string
                )
        assert excp.value.code == 'B-050-010'

    def test_block_time_with_bad_time_format_type_raises_b_050_020(self):
        """block_time_string() with bad block_format type raises SimplEthError"""
        block_num = Blockchain().block_number
        bad_format_type = 100
        with pytest.raises(SimplEthError) as excp:
            Blockchain().block_time_string(
                block_num,
                bad_format_type
                )
        assert excp.value.code == 'B-050-020'

    @pytest.mark.parametrize('bad_address',
                             ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6',
                              'xxx', 123]
                             )
    def test_is_valid_address_returns_false(self, bad_address):
        """address() with bad account_num raises SimplEthError"""
        assert Blockchain().is_valid_address(bad_address) is False

    def test_send_ether_with_too_big_amount_raises_b_070_010(self):
        """send_ether() with amount > from balance raises SimplEthError"""
        user6 = Blockchain().address(6)
        user7 = Blockchain().address(7)
        too_big_amount = Blockchain().balance(user6) + 1
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(user6, user7, too_big_amount)
        assert excp.value.code == 'B-070-010'

    @pytest.mark.parametrize('bad_address',
                             ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 'xxx']
                             )
    def test_send_ether_with_bad_address_from_raises_b_070_010(
            self,
            bad_address
            ):
        """send_ether() with bad address for from raises SimplEthError"""
        bad_address_user6 = bad_address
        user7 = Blockchain().address(7)
        amount = 2_000_000_000
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(bad_address_user6, user7, amount)
        assert excp.value.code == 'B-070-010'

    @pytest.mark.parametrize('bad_address',
                             ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 'xxx']
                             )
    def test_send_ether_with_bad_address_to_raises_b_070_010(
            self,
            bad_address
            ):
        """send_ether() with bad address for to raises SimplEthError"""
        user6 = Blockchain().address(6)
        bad_address_user7 = bad_address
        amount = 2_000_000_000
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(user6, bad_address_user7, amount)
        assert excp.value.code == 'B-070-010'

    @pytest.mark.parametrize('bad_address',
                             ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 'xxx']
                             )
    def test_send_ether_with_bad_address_from_raises_b_070_010(
            self,
            bad_address
            ):
        """send_ethers() with bad address for from raises SimplEthError"""
        bad_address_user6 = bad_address
        user7 = Blockchain().address(7)
        amount = 2_000_000_000
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(bad_address_user6, user7, amount)
        assert excp.value.code == 'B-070-010'

    def test_send_ether_with_bad_type_to_raises_b_070_020(self):
        """send_ether() with bad address for to raises SimplEthError"""
        user6 = Blockchain().address(6)
        bad_type_user7 = 123456
        amount = 2_000_000_000
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(user6, bad_type_user7, amount)
        assert excp.value.code == 'B-070-020'

    def test_send_ether_with_bad_type_from_raises_b_070_020(self):
        """send_ether() with bad address for to raises SimplEthError"""
        bad_type_user6 = 123456
        user7 = Blockchain().address(7)
        amount = 2_000_000_000
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(bad_type_user6, user7, amount)
        assert excp.value.code == 'B-070-020'

    def test_send_ether_with_float_amount_raises_b_070_020(self):
        """send_ether() with a float amount raises SimplEthError"""
        user6 = Blockchain().address(6)
        user7 = Blockchain().address(7)
        float_amount = 2_000_000_000.00
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(user6, user7, float_amount)
        assert excp.value.code == 'B-070-020'

    def test_send_ether_to_nonpayable_contract_raises_b_070_020(self):
        """send_ether() to a non-payable account raises SimplEthError"""
        # HelloWorld1 is a non-payable contract. User will attempt to
        # send ether to it.
        user0 = Blockchain().address(0)
        hello_contract = Contract('HelloWorld1')
        hello_contract.deploy(user0)
        amount = 2_000_000_000
        with pytest.raises(SimplEthError) as excp:
            Blockchain().send_ether(user0, hello_contract, amount)
        assert excp.value.code == 'B-070-020'

    @pytest.mark.parametrize('bad_hash',
                             ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 123]
                             )
    def test_transaction_with_bad_hash_raises_b_080_010(
            self,
            bad_hash
            ):
        """transaction() with bad trx_hash raises SimplEthError"""
        with pytest.raises(SimplEthError) as excp:
            Blockchain().transaction(bad_hash)
        assert excp.value.code == 'B-080-010'

    def test_transaction_with_non_hex_hash_raises_b_080_020(self):
        """transaction() with trx_hash that is not a hex value raises SimplEthError"""
        non_hex_trx_hash = 'non_hex string'
        with pytest.raises(SimplEthError) as excp:
            Blockchain().transaction(non_hex_trx_hash)
        assert excp.value.code == 'B-080-020'

    def test_trx_count_with_no_arg_raises_type_error(self):
        """Test trx_count() with no args fails."""
        with pytest.raises(TypeError):
            Blockchain().trx_count()

    def test_trx_count_with_bad_address_type_raises_b_090_010(self):
        """trx_count() with bad address raises SimplEthError"""
        bad_address_type = 200
        with pytest.raises(SimplEthError) as excp:
            Blockchain().trx_count(bad_address_type)
        assert excp.value.code == 'B-090-010'

    @pytest.mark.parametrize('bad_address',
                             ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 'xxx']
                             )
    def test_trx_count_with_bad_address_raises_b_090_020(
            self,
            bad_address
            ):
        """trx_count() with bad address raises SimplEthError"""
        with pytest.raises(SimplEthError) as excp:
            Blockchain().trx_count(bad_address)
        assert excp.value.code == 'B-090-020'

    @pytest.mark.parametrize('bad_hash',
                             ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 123]
                             )
    def test_trx_sender_with_bad_hash_raises_b_080_010(
            self,
            bad_hash
            ):
        """trx_sender() with bad trx_hash raises SimplEthError"""
        with pytest.raises(SimplEthError) as excp:
            Blockchain().trx_sender(bad_hash)
        assert excp.value.code == 'B-080-010'

    def test_trx_sender_with_non_hex_hash_raises_b_080_020(self):
        """trx_sender() with trx_hash that is not a hex value raises SimplEthError"""
        non_hex_trx_hash = 'non_hex string'
        with pytest.raises(SimplEthError) as excp:
            Blockchain().transaction(non_hex_trx_hash)
        assert excp.value.code == 'B-080-020'
    