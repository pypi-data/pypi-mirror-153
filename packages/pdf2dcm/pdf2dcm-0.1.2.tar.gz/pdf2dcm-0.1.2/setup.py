# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdf2dcm', 'pdf2dcm.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydicom>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'pdf2dcm',
    'version': '0.1.2',
    'description': 'A PDF to Dicom Converter',
    'long_description': '# pdf2dcm\n[![PyPI version](https://img.shields.io/pypi/v/pdf2dcm.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/pdf2dcm/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/pdf2dcm.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/pdf2dcm)[![Downloads](https://static.pepy.tech/personalized-badge/pdf2dcm?period=month&units=abbreviation&left_color=brightgreen&right_color=blue&left_text=PyPi%20Velocity)](https://pepy.tech/project/pdf2dcm) [![Downloads](https://static.pepy.tech/personalized-badge/pdf2dcm?period=total&units=abbreviation&left_color=brightgreen&right_color=blue&left_text=PyPi%20Downloads)](https://pepy.tech/project/pdf2dcm)\n[![codecov](https://codecov.io/gh/a-parida12/pdf2dcm/branch/main/graph/badge.svg?token=MGY9MHRP46)](https://codecov.io/gh/a-parida12/pdf2dcm)[![Test Pipeline](https://github.com/a-parida12/pdf2dcm/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/a-parida12/pdf2dcm/actions/workflows/test.yml)[![Release Pipeline](https://github.com/a-parida12/pdf2dcm/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/a-parida12/pdf2dcm/actions/workflows/release.yml)\n\nPDF to DICOM Converter\n\n> A python package for PDF to Encapsulated DCM and PDF to DICOM RGB converter\n\n## SETUP\n\nThe python package is available for use on PyPI. It can be setup simply via pip\n\n```bash\npip install pdf2dcm\n```\n\nTo the check the setup, simply check the version number of the `pdf2dcm` package by\n\n```bash\npython -c \'import pdf2dcm; print(pdf2dcm.__version__)\'\n```\n\n## PDF to Encapsulated DCM\n\n### Usage\n\n```python\nfrom pdf2dcm import Pdf2EncapsDCM\n\nconverter = Pdf2EncapsDCM()\nconverted_dcm = converter.run(path_pdf=\'tests/test_data/test_file.pdf\', path_template_dcm=\'tests/test_data/CT_small.dcm\', suffix =".dcm")\nprint(converted_dcm)\n# tests/test_data/test_file\'\n```\n\nParameters `converter.run`:\n\n- `path_pdf (str)`: path of the pdf that needs to be encapsulated\n- `path_template_dcm (str, optional)`: path to template for getting the repersonalisation of data.\n- `suffix (str, optional)`: suffix of the dicom files. Defaults to ".dcm".\n\nReturns:\n\n- `Path`: path of the stored encapsulated dcm\n\n### Notes\n\n- The name of the output dicom is same as the name of the input pdf\n- If no template is provided no repersonalisation takes place\n- It is possible to produce dicoms without a suffix by simply passing `suffix=""` to the `converter.run()`\n\n## Repersonalisation\n\nIt is the process of copying over data regarding the identity of the encapsualted pdf from a template dicom. Currently, the fileds that are repersonalised are-\n\n- PatientName\n- PatientID\n- PatientSex\n- StudyInstanceUID\n- SeriesInstanceUID\n- SOPInstanceUID\n',
    'author': 'Abhijeet Parida',
    'author_email': 'abhijeet.parida@tum.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/a-parida12/pdf2dcm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
