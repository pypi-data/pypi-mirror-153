# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frast']

package_data = \
{'': ['*']}

install_requires = \
['requests[all]>=2.27.1,<3.0.0', 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['frast = frast.main:app']}

setup_kwargs = {
    'name': 'frast',
    'version': '0.1.0',
    'description': '',
    'long_description': '# FRAST\n\nThe command line version of FRAST\nGenerates an output json file with data including MAFFT output, mutions for each sequence and related papers\n\n# frast --help\n\nUsage: frast [OPTIONS]\n\nOptions:\n--m TEXT mode of archetype selection: automatic, reference, or\ncustom [default: automatic]\n--a TEXT relative path to the custom archetype fasta file\n--i TEXT relative path to the test sequences fasta file\n[required]\n--o TEXT output file prefix (extension will be .json automatically) [default:\noutput_file]\n--help Show this message and exit.\n\n# example commands\n\n(automatically selecting archetype using input sequences)\nfrast --m automatic --i test_input.fasta --o output_file\n\n(using one of the reference archetypes by name)\nfrast --m reference --a CytB --i test_input.fasta --o output_file\n\n(using a custom archetype by fasta file)\nfrast --m custom --a test_archetype.fasta --i test_input.fasta --o output_file\n',
    'author': 'Jackson Greene',
    'author_email': 'jackson.greene@student.curtin.edu.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
