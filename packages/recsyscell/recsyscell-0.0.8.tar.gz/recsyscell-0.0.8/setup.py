from setuptools import setup
version = '0.0.8'
long_description = """Python Module for simply Colloboratioin filtering recommendation system. With use cellular automaton. You have to apply for entry Dataframe User-Item"""
setup(
    name='recsyscell',
    version=version,
    description='Binary and Regression task for simply collaboration filtering recommendation systems',
    packages=['recsyscell'],
    author_email='ryzhkov.ilya17@gmail.com',
    license='Apache License, Version 2.0, see LICENSE file',
    install_requires = ['pandas', 'numpy'],
    url="https://github.com/RyzhkovIlya/Cellular-automaton",
    download_url=f"https://github.com/RyzhkovIlya/Cellular-automaton/blob/main/Cell_automat.version{version}.zip",
    long_description=long_description)