from setuptools import setup


setup(
    name='pacote_teste_gitaction',
    version='0.0.1',
    long_description='É necessária uma descrição longa!',
    packages=['src'],
    install_requires=['httpx'],
    entry_points={
        'console_scripts': ['meu-cli = src.minha_lib:cli']
    }
)
