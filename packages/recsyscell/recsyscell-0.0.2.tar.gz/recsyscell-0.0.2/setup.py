from setuptools import setup

setup(
    name='recsyscell',
    version='0.0.2',
    description='Binary and Regression task for simply collaboration filtering recommendation systems',
    packages=['recsyscell'],
    author_email='ryzhkov.ilya17@gmail.com',
    license='Apache License, Version 2.0, see LICENSE file',
    install_requires = ['pandas', 'numpy'],
    zip_safe=False
    )