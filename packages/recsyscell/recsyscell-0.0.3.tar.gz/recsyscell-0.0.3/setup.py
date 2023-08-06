from setuptools import setup
version = '0.0.3'
setup(
    name='recsyscell',
    version=version,
    description='Binary and Regression task for simply collaboration filtering recommendation systems',
    packages=['recsyscell'],
    author_email='ryzhkov.ilya17@gmail.com',
    license='Apache License, Version 2.0, see LICENSE file',
    install_requires = ['pandas', 'numpy'],
    url="https://github.com/RyzhkovIlya/Cellular-automaton",
    download_url=f"https://github.com/RyzhkovIlya/Cellular-automaton/Cell_automat.version{version}.zip"
    )