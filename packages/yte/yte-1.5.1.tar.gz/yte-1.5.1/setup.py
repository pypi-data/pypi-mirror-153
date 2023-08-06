# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yte']

package_data = \
{'': ['*']}

install_requires = \
['dpath>=2.0,<3.0', 'plac>=1.3.4,<2.0.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['yte = yte:main']}

setup_kwargs = {
    'name': 'yte',
    'version': '1.5.1',
    'description': 'A YAML template engine with Python expressions',
    'long_description': '# YTE - A YAML template engine with Python expressions\n\n[![Docs](https://img.shields.io/badge/user-documentation-green)](https://yte-template-engine.github.io)\n[![test coverage: 100%](https://img.shields.io/badge/test%20coverage-100%25-green)](https://github.com/yte-template-engine/yte/blob/main/pyproject.toml#L30)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/yte-template-engine/yte/CI)\n![PyPI](https://img.shields.io/pypi/v/yte)\n[![Conda Recipe](https://img.shields.io/badge/recipe-yte-green.svg)](https://anaconda.org/conda-forge/yte)\n[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/yte.svg)](https://anaconda.org/conda-forge/yte)\n[![Conda Version](https://img.shields.io/conda/vn/conda-forge/yte.svg)](https://github.com/conda-forge/yte-feedstock)\n\n\nYTE is a template engine for YAML format that utilizes the YAML structure in combination with Python expressions for enabling to dynamically build YAML documents.\n\nThe key idea of YTE is to rely on the YAML structure to enable conditionals, loops and other arbitrary Python expressions to dynamically render YAML files.\nPython expressions are thereby declared by prepending them with a `?` anywhere in the YAML.\nAny such value will be automatically evaluated by YTE, yielding plain YAML as a result.\nImportantly, YTE templates are still valid YAML files (for YAML, the `?` expressions are just strings).\n\nDocumentation of YTE can be found at https://yte-template-engine.github.io.\n\n## Comparison with other engines\n\nLots of template engines are available, for example the famous generic [jinja2](https://jinja.palletsprojects.com).\nThe reasons to generate a YAML specific engine are\n\n1. The YAML syntax can be exploited to simplify template expression syntax, and make it feel less foreign (i.e. fewer special characters for control flow needed) while increasing human readability.\n2. Whitespace handling (which is important with YAML since it has a semantic there) becomes unnecessary (e.g. with jinja2, some [tuning](https://radeksprta.eu/posts/control-whitespace-in-ansible-templates) is required to obtain proper YAML rendering).\n\nOf course, YTE is not the first YAML specific template engine.\nOthers include\n\n* [Yglu](https://yglu.io)\n* [Emrichen](https://github.com/con2/emrichen)\n\nThe main difference between YTE and these two is that YTE extends YAML with plain Python syntax instead of introducing another specialized language.\nOf course, the choice is also a matter of taste.\n',
    'author': 'Johannes Köster',
    'author_email': 'johannes.koester@tu-dortmund.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yte-template-engine/yte',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
