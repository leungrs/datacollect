# coding: utf-8

from setuptools import find_packages, setup

setup(
    name='datacollect',
    version='1.0.0',
    packages=find_packages(),
    modules=["manage.py", "wsgi.py"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-excel',
        'pyexcel'
    ]
)
