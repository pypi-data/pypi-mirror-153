from importlib.metadata import entry_points
from setuptools import setup, find_packages

setup(
    name='jammi',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click==8.1.3'],
    entry_points='''
        [console_scripts]
        jammi=jammi.__main__:main
    '''
)