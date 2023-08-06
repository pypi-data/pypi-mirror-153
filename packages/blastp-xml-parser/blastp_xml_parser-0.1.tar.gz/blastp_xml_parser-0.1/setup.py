from setuptools import setup
setup(name='blastp_xml_parser',
version='0.1',
description='blastp_xml_parser',
url='https://github.com/esbusis/blastp_xml_parser.git',
author='esbusis',
author_email='esbusraisik@gmail.com',
license='MIT',
install_requires = ["biopython","pandas","more-itertools"],
packages = ['blastp_xml_parser'],
zip_safe=False)