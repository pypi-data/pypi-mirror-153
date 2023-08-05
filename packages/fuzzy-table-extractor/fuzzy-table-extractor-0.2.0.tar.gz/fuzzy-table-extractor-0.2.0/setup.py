# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzy_table_extractor',
 'fuzzy_table_extractor.handlers',
 'fuzzy_table_extractor.tests']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.3.2,<2.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'pandas>=1.3.5,<2.0.0',
 'python-docx>=0.8.11,<0.9.0',
 'pywin32>=303,<304']

setup_kwargs = {
    'name': 'fuzzy-table-extractor',
    'version': '0.2.0',
    'description': 'A tool to extract tables from documents using fuzzy matching',
    'long_description': '# Fuzzy table extractor\n## Introduction\nThis project aims to help data extraction from unstructured sources, like Word and pdf files, web documents, and so on.\n\nThe library has 2 main components: the file handler, which is responsible for identifying tables in the document and returning these in a more standarlized way; the extractor, which searches in document\'s tables and returns the one with the highest proximity, using for this a fuzzy string comparison algorithm.\n\nCurrently, there is only a handler for Docx files, but in the future, this will be expanded to other sources.\n\n## Installation\nThe library is available on PyPI:\n```\npip install fuzzy-table-extractor\n```\n\n## Using the library\n### Extracting tables\nThe usage of the library is very simple: first, a handler for the file must be created, then this object is used to create an instance of Extractor, which will contain methods for data extraction.\n\nHere is an example of table extraction for a very simple document:\n\n```python\nfrom pathlib import Path\n\nfrom fuzzy_table_extractor.handlers.docx_handler import DocxHandler\nfrom fuzzy_table_extractor.extractor import Extractor\n\nfile_path = Path(r"path_to_document.docx")\n\nhandler = DocxHandler(file_path)\nextractor = Extractor(handler)\n\ndf = extractor.extract_closest_table(search_headers=["id", "name", "age"])\nprint(df)\n```\nFor a document that looks like this:\n\n![Basic document](https://github.com/LeonardoSirino/FuzzyTableExtractor/blob/main/assets/basic_document.png?raw=true)\n\nThe output is:\n```\n  id  name age\n0  0  Paul  25\n1  1  John  32\n```\n\nDue to the fuzzy match used to select the closest table, even though the search headers do not exactly match a table header in the document, the extraction will return the right table if this is the closest to the search, which also makes the extraction resilient to typos. As an example, using the same code above, but now for a document like this:\n\n![Typos in document](https://github.com/LeonardoSirino/FuzzyTableExtractor/blob/main/assets/typos_in_document.png?raw=true)\nThe output is:\n```\n  id  name age\n0  0  Paul  25\n1  1  John  32\n2  2   Bob  56\n```\n### Extracting single field\nThere is also the possibility to extract only a single field (cell) from a document. Here is an example of how to do this with the library:\n\n```python\nfrom pathlib import Path\n\nfrom fuzzy_table_extractor.handlers.docx_handler import DocxHandler\nfrom fuzzy_table_extractor.extractor import Extractor, FieldOrientation\n\nfile_path = Path(r"path_to_document.docx")\n\nhandler = DocxHandler(file_path)\nextractor = Extractor(handler)\n\narea = extractor.extract_single_field(field="area", \n                                      orientation=FieldOrientation.ROW)\nprint(area)\n```\n\nFor a document like this:\n![Extracting single field](https://github.com/LeonardoSirino/FuzzyTableExtractor/blob/main/assets/extract_single_field.png?raw=true)\n\nThe output is:\n```\n430.9 km2\n```\n\nThe file [examples.py](https://github.com/LeonardoSirino/FuzzyTableExtractor/blob/main/examples.py) contains other examples of how to use the library\n\n\n## TODO\n- [ ] Add to README a guide on how to contribute to project\n- [ ] Expand test coverage\n- [ ] Create a handler for pdf files\n',
    'author': 'Leonardo Sirino',
    'author_email': 'leonardosirino@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LeonardoSirino/FuzzyTableExtractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
