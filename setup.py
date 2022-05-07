from setuptools import setup, find_packages

setup(
    name='chessiq',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "berserk-downstream==0.11.9",
        "chess==1.9.0",
        "click==8.1.3",
    ],
    entry_points={
        'console_scripts': [
            'chessiq = chessiq.cli:cli',
        ],
    },
)