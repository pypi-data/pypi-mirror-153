# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncbiutils']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'lxml>=4.8.0,<5.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'ncbiutils',
    'version': '0.5.1',
    'description': 'Retrieve article records from NCBI via E-utilities',
    'long_description': '# ncbiutils\n\n![build](https://github.com/PathwayCommons/ncbiutils/actions/workflows/build.yml/badge.svg)\n[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/PathwayCommons/ncbiutils/LICENSE)\n[![codecov](https://codecov.io/gh/PathwayCommons/ncbiutils/branch/main/graph/badge.svg?token=CFD1jGfNKl)](https://codecov.io/gh/PathwayCommons/ncbiutils)\nMaking retrieval of records from [National Center for Biotechnology Information (NCBI)](https://www.ncbi.nlm.nih.gov/) [E-Utilities](https://www.ncbi.nlm.nih.gov/books/NBK25499/) simpler.\n\n## Installation\n\nSet up a virtual environment. Here, we use [miniconda](https://docs.conda.io/en/latest/miniconda.html) to create an environment named `testenv`:\n\n```bash\n$ conda create --name testenv python=3.8\n$ conda activate testenv\n```\n\nThen install the package in the `testenv` environment:\n\n```bash\n$ pip install ncbiutils\n```\n\n## Usage\n\nThe `ncbiutils` module exposes a `PubMedFetch` class that provides an easy to configure and use wrapper for the [EFetch](https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.EFetch) E-Utility. By default, `PubMedFetch` will retrieve PubMed article records, each indicated by its PubMed identifier (PMID).\n\n```python\nfrom ncbiutils.ncbiutils import PubMedFetch\n\n# Initalize a list of PubMed identifiers for those records we wish to retrieve\nuids = [\'16186693\', \'29083299\']\n\n# Create an instance, optionally provide an E-Utility API key\npubmed_fetch = PubMedFetch()\n\n# Retrieve the records\n# Returns a generator that yields results for a chunk of the input PMIDs (see Options)\nchunks = pubmed_fetch.get_citations(uids)\n\n# Iterate over the results\nfor chunk in chunks:\n    # A Chunk is a namedtuple with 3 fields:\n    #   - error: Includes network errors as well as HTTP status >=400\n    #   - citations: article records, each wrapped as a Citation\n    #   - ids: input ids for chunk\n    error, citations, ids = chunk\n\n    # Citation class can be represented as a dict\n    print(citations[0].dict())\n```\n\n*Options*\n\nConfigure the `PubMedFetch` instance through its constructor:\n\n- retmax : int\n  - Maximum number of records to return in a chunk (default/max 10000)\n- api_key : str\n  - API key for NCBI E-Utilities\n\n---\n\nAlso available is `PubMedDownload` that can retrieve records from the PubMed FTP server for both [baseline and daily updates](https://pubmed.ncbi.nlm.nih.gov/download/).\n\n## Testing\n\nAs this project was built with [poetry](https://python-poetry.org), you\'ll need to [install poetry](https://python-poetry.org/docs/#installation) to get this project\'s development dependencies.\n\nOnce installed, clone this GitHub remote:\n\n```bash\n$ git clone https://github.com/PathwayCommons/ncbiutils\n$ cd ncbiutils\n```\n\nInstall the project:\n\n```bash\n$ poetry install\n```\n\nRun the test script:\n\n```bash\n$ ./test.sh\n```\n\nUnder the hood, the tests are run with [pytest](https://docs.pytest.org/). The test script also does a lint check with [flake8](https://flake8.pycqa.org/) and type check with [mypy](http://mypy-lang.org/).\n\n\n## Publishing a release\n\nA GitHub workflow will automatically version and release this package to [PyPI](https://pypi.org/) following a push directly to `main` or when a pull request is merged into `main`. A push/merge to `main` will automatically bump up the patch version.\n\nWe use [Python Semantic Release (PSR)](https://python-semantic-release.readthedocs.io/en/latest/) to manage versioning. By making a commit with a well-defined message structure, PSR will scan commit messages and bump the version accordingly in accordance with [semver](https://python-poetry.org/docs/cli/#version).\n\nFor a patch bump:\n\n```bash\n$ git commit -m "fix(ncbiutils): some comment for this patch version"\n```\n\nFor a minor bump:\n\n```bash\n$ git commit -m "feat(ncbiutils): some comment for this minor version bump"\n```\n\nFor a release:\n\n```bash\n$ git commit -m "feat(mod_plotting): some comment for this release\\n\\nBREAKING CHANGE: other footer text."\n```\n',
    'author': 'Biofactoid',
    'author_email': 'support@biofactoid.org',
    'maintainer': 'Biofactoid',
    'maintainer_email': 'support@biofactoid.org',
    'url': 'https://github.com/PathwayCommons/ncbiutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
