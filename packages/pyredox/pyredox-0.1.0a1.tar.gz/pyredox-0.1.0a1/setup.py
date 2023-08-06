# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyredox',
 'pyredox.claim',
 'pyredox.clinicaldecisions',
 'pyredox.clinicalsummary',
 'pyredox.device',
 'pyredox.financial',
 'pyredox.flowsheet',
 'pyredox.generic',
 'pyredox.inventory',
 'pyredox.media',
 'pyredox.medications',
 'pyredox.notes',
 'pyredox.order',
 'pyredox.organization',
 'pyredox.patientadmin',
 'pyredox.patienteducation',
 'pyredox.patientsearch',
 'pyredox.provider',
 'pyredox.referral',
 'pyredox.research',
 'pyredox.results',
 'pyredox.scheduling',
 'pyredox.sso',
 'pyredox.surgicalscheduling',
 'pyredox.vaccination']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<1.10.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

setup_kwargs = {
    'name': 'pyredox',
    'version': '0.1.0a1',
    'description': '',
    'long_description': '# Pyredox - A Pydantic-Based Library for Redox Data\n\n[![PyPI Info](https://img.shields.io/pypi/v/pyredox.svg)](https://pypi.python.org/pypi/pyredox)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/cedar-team/pyredox/main)](https://github.com/cedar-team/pyredox/actions)\n[![Coverage Info](https://coveralls.io/repos/github/cedar-team/pyredox/badge.svg?branch=main)](https://coveralls.io/github/cedar-team/pyredox?branch=main)\n[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPyredox is library for producing, ingesting, and validating data from [Redox], a\n"data platform designed to connect providers, payers and products."\n\nPyredox is a set of [Pydantic] models that conforms to the [Redox data model]\nspecification for the purpose of making it easy to convert Redox-formatted JSON to\nPython objects and vice versa. Because pyredox inherits the functionality of\nPydantic, it validates that the JSON data conforms to the spec automatically upon\nobject creation.\n\nFor example, if you tried to create a [`NewPatient`\nmodel](https://developer.redoxengine.com/data-models/PatientAdmin.html#NewPatient) with\ninsufficient data, you would get an error like this:\n\n```python\n>>> from pyredox.patientadmin.newpatient import NewPatient\n>>> NewPatient(Meta={})\n\nValidationError: 3 validation errors for NewPatient\nMeta -> DataModel\n  field required (type=value_error.missing)\nMeta -> EventType\n  field required (type=value_error.missing)\nPatient\n  field required (type=value_error.missing)\n```\n\n\n## Usage\n\nThe simplest way to create a `pyredox` model from a JSON payload is to pass an\nunpacked `dict` as the parameter when initializing the object, like this:\n\n```python\npayload_str = """\n{\n   "Meta": {\n      "DataModel": "PatientAdmin",\n      "EventType": "NewPatient"\n   },\n   "Patient": {\n      "Identifiers": [\n         {\n            "ID": "e167267c-16c9-4fe3-96ae-9cff5703e90a",\n            "IDType": "EHRID"\n         }\n      ]\n   }\n}\n"""\ndata = json.loads(payload_str)\nnew_patient = NewPatient(**data)\n```\n\nIf you have a payload and don\'t know which object type it is, you can use the\nfactory helper, which can take a JSON string or the loaded JSON dict/list:\n\n```python\nfrom pyredox.factory import redox_object_factory\n\nredox_object1 = redox_object_factory(payload_str)  # str input\nredox_object2 = redox_object_factory(data)  # dict input\n```\n\nTo create a JSON payload to send to Redox from an existing `pyredox` object, just\ncall the `json()` method of the object:\n\n```python\nnew_patient.json()\n```\n\nWhen working with the individual fields of a model object, you can traverse the\nelement properties like so:\n\n```python\nnew_patient.patient.identifiers[0].id  # "e167267c-16c9-4fe3-96ae-9cff5703e90a"\n```\n\n\n[Redox]: https://www.redoxengine.com/\n[Redox data model]: https://developer.redoxengine.com/data-models/index.html\n[Pydantic]: https://pydantic-docs.helpmanual.io/\n',
    'author': 'Mike Mabey',
    'author_email': 'mike.mabey@cedar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cedar-team/pyredox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
