"""Test Convert() methods"""
import pytest
import time
import re

from simpleth import Blockchain, Convert, SimplEthError


# Ether denomination names to their value in wei
d2w = {
    'wei': 1,
    'kwei': 10**3,
    'babbage': 10**3,
    'femtoether': 10**3,
    'mwei': 10**6,
    'lovelace': 10**6,
    'picoether': 10**6,
    'gwei': 10**9,
    'shannon': 10**9,
    'nanoether': 10**9,
    'nano': 10**9,
    'szabo': 10**12,
    'microether': 10**12,
    'micro': 10**12,
    'finney': 10**15,
    'milliether': 10**15,
    'milli': 10**15,
    'ether': 10**18,
    'kether': 10**21,
    'grand': 10**21,
    'mether': 10**24,
    'gether': 10**27,
    'tether': 10**30
    }


# Test this first. Insure it is accurate and then test convert_ether().
def test_denominations_to_wei():
    """Return dictionary of denomination names and value in wei"""
    assert Convert().denominations_to_wei() == d2w


# This is a brute force test. It generates 23x23 test cases. These
# take about 50 seconds on my laptop to run.
@pytest.mark.skip(reason='takes too long')
@pytest.mark.parametrize('from_denominations', [
        'wei',
        'kwei',
        'babbage',
        'femtoether',
        'mwei',
        'lovelace',
        'picoether',
        'gwei',
        'shannon',
        'nanoether',
        'nano',
        'szabo',
        'microether',
        'micro',
        'finney',
        'milliether',
        'milli',
        'ether',
        'kether',
        'grand',
        'mether',
        'gether',
        'tether'
        ]
    )
@pytest.mark.parametrize('to_denominations', [
        'wei',
        'kwei',
        'babbage',
        'femtoether',
        'mwei',
        'lovelace',
        'picoether',
        'gwei',
        'shannon',
        'nanoether',
        'nano',
        'szabo',
        'microether',
        'micro',
        'finney',
        'milliether',
        'milli',
        'ether',
        'kether',
        'grand',
        'mether',
        'gether',
        'tether'
        ]
    )
def test_convert_ether_all(from_denominations, to_denominations):
    """convert_ether() returns accurate conversion for all combinations of
    to and from denominations"""
    amount = 10
    # Validate with web3.py conversion methods
    converted_amount = Blockchain().web3.fromWei(
        Blockchain().web3.toWei(amount, from_denominations),
        to_denominations
        )
    assert Convert().convert_ether(
        amount,
        from_denominations,
        to_denominations
        ) == converted_amount


@pytest.mark.parametrize('bad_denominations', ['xxx', 1234])
def test_convert_ether_bad_from(bad_denominations):
    """convert_ether() with bad from denomination raises SimplEthError"""
    with pytest.raises(SimplEthError) as excp:
        Convert().convert_ether(10, bad_denominations, 'ether')
    assert excp.value.code == 'V-010-010'


@pytest.mark.parametrize('bad_denominations', ['xxx', 1234])
def test_convert_ether_bad_to(bad_denominations):
    """convert_ether() with bad to denomination raises SimplEthError"""
    with pytest.raises(SimplEthError) as excp:
        Convert().convert_ether(10, 'ether', bad_denominations)
    assert excp.value.code == 'V-010-020'


def test_epoch_time():
    """epoch_time() returns a float and value increases over time"""
    t1 = Convert().epoch_time()
    time.sleep(.01)
    t2 = Convert().epoch_time()
    assert isinstance(t1, float) and (t2 > t1)


def test_local_time_string():
    """local_time_string() returns a formatted time string"""
    # default time string format:  YYYY-MM-DD HH:MM:SS
    default_time_format = \
        "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}"
    assert(
        re.match(
            default_time_format,
            Convert().local_time_string()
            )
        )


def test_local_time_with_time_format():
    """local_time() returns a specified formatted time string"""
    strftime = '%I:%M'    # use a simple time string format of HH:MM
    time_format = "[0-9]{2}:[0-9]{2}"
    assert(
        re.match(
            time_format,
            Convert().local_time_string(strftime)
            )
        )


def test_local_time_string_raises_v_020_010():
    """local_time_string() with bad t_format type raises SimplEthError"""
    bad_format_type = 100
    with pytest.raises(SimplEthError) as excp:
        Convert().local_time_string(bad_format_type)
    assert excp.value.code == 'V-020-010'


def test_to_local_time_string_int():
    """to_local_time_string() with integer epoch seconds returns a
    formatted time string"""
    time_format = '%Y-%m-%d %H:%M:%S'  # must match simpleth TIME_FORMAT
    test_epoch_sec = 1639932637
    test_local_time = time.strftime(
        time_format,
        time.localtime(test_epoch_sec)
        )
    assert(
        Convert().to_local_time_string(test_epoch_sec) == test_local_time
        )


def test_to_local_time_string_float():
    """to_local_time_string() returns a float epoch seconds returns a
    formatted time string"""
    time_format = '%Y-%m-%d %H:%M:%S'  # must match simpleth TIME_FORMAT
    test_epoch_sec = 1639932637.00
    test_local_time = time.strftime(
        time_format,
        time.localtime(test_epoch_sec)
        )
    assert(
        Convert().to_local_time_string(test_epoch_sec) == test_local_time
        )


def test_to_local_time_with_time_format():
    """to_local_time() returns a specified formatted time string"""
    t_format = '%I:%M'    # use a simple time string format of HH:MM
    test_epoch_sec = 1639932637
    test_local_time = time.strftime(
        t_format,
        time.localtime(test_epoch_sec)
        )
    assert(
        Convert().to_local_time_string(test_epoch_sec, t_format) ==
        test_local_time
        )


def test_to_local_time_string_raises_v_030_010():
    """to_local_time_string() with bad t_format type raises SimplEthError"""
    bad_format_type = 100
    test_epoch_sec = 1639932637
    with pytest.raises(SimplEthError) as excp:
        Convert().to_local_time_string(test_epoch_sec, bad_format_type)
    assert excp.value.code == 'V-030-010'
