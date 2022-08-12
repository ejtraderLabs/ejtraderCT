__all__ = ['calculate_commission', 'calculate_pip_value', 'calculate_spread']


def calculate_spread(bid: str, ask: str, pip_position: int) -> int:
    spread = float(ask) - float(bid)
    spread = '{:.{}f}'.format(spread, pip_position + 1)
    return int(spread.replace('.', ''))


def calculate_pip_value(price: str, size: int, pip_position: int) -> str:
    pip = (pow(1 / 10, pip_position) * size) / float(price)
    pip = '{:.5f}'.format(pip)
    return pip


def calculate_commission(size=10000, rate=1, commission=0.000030):
    # can't handle different size/rate for now
    return (size * commission) * rate * 2