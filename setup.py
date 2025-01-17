from setuptools import setup, find_packages

setup(
    name='chessiq',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "berserk-downstream",
        "chess",
        "click",
        "requests",
        "pyyaml",
        "nltk",
        "chess.com",
        "Cython==3.0.7"
    ],
    entry_points={
        'console_scripts': [
            'chessiq = chessiq.cli:cli',
        ],
    },
)