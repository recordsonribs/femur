from setuptools import setup, find_packages

import femur


setup(
    name='femur',
    version=femur.__version__,
    description=femur.__doc__.strip(),
    long_description=open('readme.md').read(),
    url='https://github.com/recordsonribs/femur',
    license=femur.__license__,
    author=femur.__author__,
    author_email='alex@recordsonribs.com',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    scripts=[
        'bin/femur',
    ],
)
