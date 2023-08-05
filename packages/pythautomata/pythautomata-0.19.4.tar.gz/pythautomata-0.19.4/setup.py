# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythautomata',
 'pythautomata.abstract',
 'pythautomata.automata',
 'pythautomata.automata.wheighted_automaton_definition',
 'pythautomata.automata_definitions',
 'pythautomata.base_types',
 'pythautomata.boolean_algebra_learner',
 'pythautomata.exceptions',
 'pythautomata.guards',
 'pythautomata.model_comparators',
 'pythautomata.model_exporters',
 'pythautomata.regular_expressions',
 'pythautomata.tests',
 'pythautomata.utilities']

package_data = \
{'': ['*']}

install_requires = \
['graphviz', 'numpy', 'scipy>=1.7.3,<2.0.0', 'sklearn>=0.0,<0.1']

setup_kwargs = {
    'name': 'pythautomata',
    'version': '0.19.4',
    'description': "ORT's implementation of various kinds of automata",
    'long_description': '# Pythautomata\n\nPythautomata is a Python library for modeling finite state systems.\n\n## A**bout**\nPythautomata is developed at the [](http://www.cs.tu-dortmund.de/)Department of Artificial Intelligence and Big Data of the Universidad ORT Uruguay. Its main goal is to provide implementations for the structures needed for working in the Model Extraction Framework.\n\nModels present in the framework are:\n\n- DFA\n- NFA\n- WFA/PDFA\n- SFA\n\nAll of these can be exported in different manners, like pickle or to visual representations using Graphviz. Besides the structure representations a number of algorithms of interest are implemented, to name a few:\n\n- FSA minimization\n- FSA comparison using Hopcroft Karp equivalence\n- FSA intersection (and other boolean operations)\n\n\n## **Installation**\n\n```\npip install pythautomata\n```\n\n\n\n## **Documentation**\n\n- [**API Documentation:**](https://neuralchecker.github.io/pythautomata/index.html)\n\n\n## **Maintainers**\n\nFederico Vilensky\n\nFranz Mayr\n\nFederico Pan\n\n\n## Colaborators\n',
    'author': 'Federico Vilensky',
    'author_email': 'fedevilensky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
