# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['concise_concepts',
 'concise_concepts.conceptualizer',
 'concise_concepts.examples']

package_data = \
{'': ['*']}

install_requires = \
['gensim>=4,<5', 'spacy>=3,<4']

setup_kwargs = {
    'name': 'concise-concepts',
    'version': '0.5.4',
    'description': 'This repository contains an easy and intuitive approach to few-shot NER using most similar expansion over spaCy embeddings. Now with entity confidence scores!',
    'long_description': '# Concise Concepts\nWhen wanting to apply NER to concise concepts, it is really easy to come up with examples, but pretty difficult to train an entire pipeline. Concise Concepts uses few-shot NER based on word embedding similarity to get you going with easy! Now with entity scoring!\n\n[![Python package](https://github.com/Pandora-Intelligence/concise-concepts/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/Pandora-Intelligence/concise-concepts/actions/workflows/python-package.yml)\n[![Current Release Version](https://img.shields.io/github/release/pandora-intelligence/concise-concepts.svg?style=flat-square&logo=github)](https://github.com/pandora-intelligence/concise-concepts/releases)\n[![pypi Version](https://img.shields.io/pypi/v/concise-concepts.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/concise-concepts/)\n[![PyPi downloads](https://static.pepy.tech/personalized-badge/concise-concepts?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/concise-concepts/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)\n\n\n# Install\n\n```\npip install concise-concepts\n```\n\n# Tutorials\n\n[TechVizTheDataScienceGuy](https://www.youtube.com/c/TechVizTheDataScienceGuy) created a [nice tutorial](https://prakhar-mishra.medium.com/few-shot-named-entity-recognition-in-natural-language-processing-92d31f0d1143) on how to use it.\n\n[I](https://www.linkedin.com/in/david-berenstein-1bab11105/) created a [tutorial](https://www.rubrix.ml/blog/concise-concepts-rubrix/) in collaboration with Rubrix.\n\n# Quickstart\n\n```python\nimport spacy\nfrom spacy import displacy\nimport concise_concepts\n\ndata = {\n    "fruit": ["apple", "pear", "orange"],\n    "vegetable": ["broccoli", "spinach", "tomato"],\n    "meat": ["beef", "pork", "fish", "lamb"]\n}\n\ntext = """\n    Heat the oil in a large pan and add the Onion, celery and carrots. \n    Then, cook over a medium–low heat for 10 minutes, or until softened. \n    Add the courgette, garlic, red peppers and oregano and cook for 2–3 minutes.\n    Later, add some oranges and chickens. """\n\nnlp = spacy.load("en_core_web_lg", disable=["ner"])\n# ent_score for entity condifence scoring\nnlp.add_pipe("concise_concepts", config={"data": data, "ent_score": True})\ndoc = nlp(text)\n\noptions = {"colors": {"fruit": "darkorange", "vegetable": "limegreen", "meat": "salmon"},\n           "ents": ["fruit", "vegetable", "meat"]}\n\nents = doc.ents\nfor ent in ents:\n    new_label = f"{ent.label_} ({float(ent._.ent_score):.0%})"\n    options["colors"][new_label] = options["colors"].get(ent.label_.lower(), None)\n    options["ents"].append(new_label)\n    ent.label_ = new_label\ndoc.ents = ents\n\ndisplacy.render(doc, style="ent", options=options)\n```\n![](https://raw.githubusercontent.com/Pandora-Intelligence/concise-concepts/master/img/example.png)\n\n## use specific number of words to expand over\n\n```python\ndata = {\n    "fruit": ["apple", "pear", "orange"],\n    "vegetable": ["broccoli", "spinach", "tomato"],\n    "meat": ["beef", "pork", "fish", "lamb"]\n}\n\ntopn = [50, 50, 150]\n\nassert len(topn) == len\n\nnlp.add_pipe("concise_concepts", config={"data": data, "topn": topn})\n````\n\n## use word similarity to score entities\n\n```python\nimport spacy\nimport concise_concepts\n\ndata = {\n    "ORG": ["Google", "Apple", "Amazon"],\n    "GPE": ["Netherlands", "France", "China"],\n}\n\ntext = """Sony was founded in Japan."""\n\nnlp = spacy.load("en_core_web_lg")\nnlp.add_pipe("concise_concepts", config={"data": data, "ent_score": True})\ndoc = nlp(text)\n\nprint([(ent.text, ent.label_, ent._.ent_score) for ent in doc.ents])\n# output\n#\n# [(\'Sony\', \'ORG\', 0.63740385), (\'Japan\', \'GPE\', 0.5896993)]\n````\n\n## use gensim.word2vec model from pre-trained gensim or custom model path\n\n```python\ndata = {\n    "fruit": ["apple", "pear", "orange"],\n    "vegetable": ["broccoli", "spinach", "tomato"],\n    "meat": ["beef", "pork", "fish", "lamb"]\n}\n\n# model from https://radimrehurek.com/gensim/downloader.html or path to local file\nmodel_path = "glove-twitter-25"\n\nnlp.add_pipe("concise_concepts", config={"data": data, "model_path": model_path})\n````\n',
    'author': 'David Berenstein',
    'author_email': 'david.m.berenstein@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pandora-intelligence/concise-concepts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
