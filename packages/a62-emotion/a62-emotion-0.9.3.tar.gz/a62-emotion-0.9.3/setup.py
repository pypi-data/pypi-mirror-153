# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emotion',
 'emotion.cli',
 'emotion.data',
 'emotion.features',
 'emotion.models',
 'emotion.train',
 'emotion.visualization']

package_data = \
{'': ['*']}

install_requires = \
['dvc[gdrive]<2.11',
 'keras>=2.8.0,<3.0.0',
 'numpy==1.20.3',
 'pandas==1.2.4',
 'scikit-learn==0.24.2']

entry_points = \
{'console_scripts': ['emotion = emotion.cli:cli']}

setup_kwargs = {
    'name': 'a62-emotion',
    'version': '0.9.3',
    'description': 'A model for emotion classification based on text and audio.',
    'long_description': '# Emotion\n\nA model for emotion classification based on text and audio.\n\n[![emotion - merge](https://github.com/philipGaudreau/emotion/actions/workflows/merge.yml/badge.svg)](https://github.com/philipGaudreau/emotion/actions/workflows/merge.yml)\n[![emotion - pr](https://github.com/philipGaudreau/emotion/actions/workflows/pr.yml/badge.svg?event=pull_request)](https://github.com/philipGaudreau/emotion/actions/workflows/pr.yml)\n[![emotion - push](https://github.com/philipGaudreau/emotion/actions/workflows/push.yml/badge.svg?event=push)](https://github.com/philipGaudreau/emotion/actions/workflows/push.yml)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n\n## Acknowledgements\n\n - Hafed Benteftifa\n - Soumaya Chaffar\n\n## Features\n\nGive audio and text as input and get back the dominant emotion.\n\n## Usage/Examples\n\n```python\n[TODO]\n```\n\n## API Reference [TODO]\n\n#### Get all items\n\n```http\n  GET /api/items\n```\n\n| Parameter | Type     | Description                |\n| :-------- | :------- | :------------------------- |\n| `api_key` | `string` | **Required**. API key      |\n\n#### Get item\n\n```http\n  GET /api/items/${id}\n```\n\n| Parameter | Type     | Description                       |\n| :-------- | :------- | :-------------------------------- |\n| `id`      | `string` | **Required**. Id of item to fetch |\n\n## Installation\n\nInstall emotion with pip\n\n```bash\n  pip install emotion\n```\n\n## Environment Variables\n\nTo run this project, you will need to add the following environment variables to your .env file\n\n`GDRIVE_CREDENTIALS_DATA`\n\n`SECRET_KEY`\n\n## Run Locally\n\nBe sure to have python 3.8 as the python executable\n```bash\npython3 --version\n```\n\nTo install Poetry, run:\n```bash\ncurl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0b1 python3 - --yes\n```\n\nClone the project\n\n```bash\ngit clone https://github.com/philipgaudreau/emotion\n```\n\nGo to the project directory\n\n```bash\ncd emotion\n```\n\nInstall dependencies (add flag `--default` if you do not want development dependencies)\n\n```bash\npoetry install\n```\n\nActivate the virtual environment\n\n```bash\npoetry shell\n```\n\nStart using the command line interface\n\n```bash\nemotion --help\n```\n\n## Running Tests\n\nTo run tests, run the following command (development dependencies must be installed)\n\n```bash\npytest tests\n```\n\n## Deployment\n\nTo deploy this project run\n\n```bash\n[TODO]\n```\n\n## Tech Stack\n\n**Client:** flask, [TODO]\n\n**Server:** python,  [TODO]\n## Feedback\n\nIf you have any feedback, please reach out to one of us.\n\n\n## Authors\n\n- [@philipgaudreau](https://github.com/philipgaudreau)\n- [@guraymo](https://github.com/guraymo)\n- [@gtrottier](https://github.com/gtrottier)\n\n\n## 🚀 About Us\nWe are on our way to finish a degree in Machine Learning.\n\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n',
    'author': 'Philip Gaudreau',
    'author_email': 'this@philipgaudreau.email',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/philipgaudreau/emotion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
