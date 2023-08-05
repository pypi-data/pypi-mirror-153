from setuptools import setup

setup(
    name='GetBourse',
    version='0.1.1',
    description='A Bourse Analysis Library  , Sponser: peyman6996',
    author='Hossein Sayedmousavi',
    author_email='Hossein.Sayyedmousavi@gmail.com',
    packages=['GetBourse'],
    install_requires=['pandas',
                      'requests',
                      'bs4',
                      'setuptools',
                      'openpyxl'
                      ]
)