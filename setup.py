"""The python wrapper for Ctrader FIX API package setup."""
from setuptools import (setup, find_packages)


setup(
    name="ejtrader_ct",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["pylint","requests","websocket-client==0.56"],
    include_package_data = True,
    description="Ctrader FIX API for python",
    long_description="Ctrader FIX API for python",
    url="https://github.com/traderpedroso/ejtrader_ct",
    author="Emerson Pedroso & Douglas Barros",
    author_email="emerson@sostrader.com.br",
    zip_safe=False
)