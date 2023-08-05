# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlptest', 'nlptest.performers']

package_data = \
{'': ['*']}

install_requires = \
['overrides>=6.1.0,<7.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'sentencepiece>=0.1.96,<0.2.0',
 'torch>=1.11.0,<2.0.0',
 'transformers>=4.18.0,<5.0.0']

setup_kwargs = {
    'name': 'nlptest',
    'version': '0.1.0',
    'description': '🧪 Behavioral tests for NLP models 🧪',
    'long_description': '<img src="figures/NLPtest.png" width="50%" align="right"/>\n\n# NLPtest\n\n**NLPtest** is Python package designed to ease *behavioral testing* of Natural Language Processing models to identify\npossible capability failures.\n\n## 1. About the project\n\nBehavioral tests are intended to test a model against some input data while treating as a black box. The aim is to\nobserve the model\'s reaction against some perturbations that might occur once the model is productionized. For a more\ndetailed explanation on behavioral testing of NLP models I encourage you to read the insightful\npaper: [Beyond Accuracy: Behavioral Testing of NLP models with CheckList](https://arxiv.org/abs/2005.04118)\n\n**NLPtest** provides helper objects for three different aspects:\n\n- easily generate text samples\n- test some specific behaviors of your model\n- aggregate the tests outcomes of your model\n\n## 2. Getting started\n\n### 2.1. Installation\n\nYou can directly install **NLPtest** using [pypi](https://pypi.org/project/nlptest/):\n\n```\npip3 install nlptest\n```\n\n### 2.2. Usage\n\nTo help you get the hang of the library we provide three different Notebooks to the user, accessible from the `examples/` folder:\n\n1. `Samples_generation.ipynb`: shows you how to easily generate texts using the `Generator` object.\n2. `Please_Behave.ipynb`: getting familiar with the `Behavior` object.\n3. `End2End_tests.ipynb`: how to run tests and get an overview of your model behavior.\n\n# References\n\nBelow, you can find resources that were used for the creation of **NLPtest** as well as relevant resources about\nbehavioral testing.\n\n* [MadeWithML](https://madewithml.com/courses/mlops/testing/#behavioral-testing)\n* [CheckList](https://github.com/marcotcr/checklist)\n* [Beyond Accuracy: Behavioral Testing of NLP models with CheckList](https://arxiv.org/abs/2005.04118)',
    'author': 'JulesBelveze',
    'author_email': 'jules.belveze@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JulesBelveze/nlptest',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
