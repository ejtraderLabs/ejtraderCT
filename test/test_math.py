from ejtraderCT import calculate_spread, calculate_pip_value, calculate_commission


def test_spread():
    assert calculate_spread('113', '113.015', 2) == 15
    assert calculate_spread('1.09553', '1.09553', 4) == 0
    assert calculate_spread('9.59', '10', 1) == 41
    assert calculate_spread('113.1', '113.2', 2) == 100


def test_pip_value():
    assert calculate_pip_value('19.00570', 100000, 4) == '0.52616'
    assert calculate_pip_value('1.3348', 100000, 4) == '7.49176'
    assert calculate_pip_value('112.585', 10000, 2) == '0.88822'


def test_commission():
    assert calculate_commission(10000, 1, 0.000030) == 0.6


