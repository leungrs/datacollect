# coding: utf-8

from setuptools import find_packages, setup

setup(
    name='datacollect',
    version='1.0.0',
    maintainer='Winson.Liang',
    maintainer_email='lai_mosi@126.com',
    description='数据采集',
    long_description='数据采集',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)
