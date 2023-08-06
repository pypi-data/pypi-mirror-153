# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thousandwords']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.21.34,<2.0.0',
 'click>=7.1.2',
 'ipython>=5.5.0',
 'nanoid>=2.0.0,<3.0.0',
 'pyflakes>=2.4.0,<3.0.0',
 'python-graphql-client>=0.4.3,<0.5.0',
 'requests-aws4auth>=1.1.2,<2.0.0',
 'requests>=2.23.0',
 'thousandwords.core>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['thousandwords = thousandwords.cli:main']}

setup_kwargs = {
    'name': 'thousandwords',
    'version': '0.10.0',
    'description': 'Share your code, data and visuals, directly from Jupyter',
    'long_description': '# thousandwords\n\n- Documentation: https://docs.1000words-hq.com/\n- 1000Words Home: https://1000words-hq.com/\n- Try it in Colab: https://colab.research.google.com/drive/1E5oU6TjH6OocmvEfU-foJfvCTbTfQrqd?usp=sharing\n',
    'author': 'Edouard Godfrey',
    'author_email': 'edouard@1000words-hq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://1000words-hq.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
