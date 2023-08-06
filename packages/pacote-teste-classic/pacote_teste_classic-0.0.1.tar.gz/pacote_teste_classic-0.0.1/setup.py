
from gettext import install
from importlib_metadata import entry_points
from setuptools import setup


setup(
    name='pacote_teste_classic',
    version='0.0.1',
    packages=['pacote'],
    install_requires=['httpx'],
    entry_points={
        'console_scripts': ['meu-cli = pacote.minha_lib:cli']
    }
)
