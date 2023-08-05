# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bentoctl',
 'bentoctl.cli',
 'bentoctl.operator',
 'bentoctl.operator.utils',
 'bentoctl.utils',
 'bentoctl.utils.operator_helpers']

package_data = \
{'': ['*']}

install_requires = \
['PyYaml>=6,<7',
 'bentoml==1.0.0a7',
 'cerberus>=1,<2',
 'click>=8,<9',
 'docker>=5,<6',
 'rich',
 'semantic_version>=2.9.0,<3.0.0',
 'simple-term-menu==0.4.4']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['bentoctl = bentoctl.cli:bentoctl']}

setup_kwargs = {
    'name': 'bentoctl',
    'version': '0.2.3',
    'description': 'Fast model deployment with BentoML on cloud platforms.',
    'long_description': '<div align="center">\n  <h1>bentoctl</h1>\n  <i>Fast model deployment with BentoML on cloud platforms</i>\n  <p>\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/bentoctl?style=flat-square">\n    <img alt="GitHub branch checks state" src="https://img.shields.io/github/checks-status/bentoml/bentoctl/main?style=flat-square">\n    <img alt="Codecov" src="https://img.shields.io/codecov/c/github/bentoml/bentoctl?style=flat-square">\n</p>\n</div>\n\n<br>\n\n`bentoctl` is a CLI tool for deploying your machine-learning models to any cloud platforms. It built on top of [BentoML: the unified model serving framework](https://github.com/bentoml/BentoML), and makes it easy to bring any BentoML packaged model to production.\n\n👉 [Pop into our Slack community!](https://l.linklyhq.com/l/ktPp) We\'re happy to help with any issue you face or even just to meet you and hear what you\'re working on :)\n\n## Features:\n\n* Supports major cloud providers: AWS, Azure, Google Cloud, and more.\n* Easy to deploy, update and reproduce model deployments.\n* First class integration with Terraform.\n* Optimized for CI/CD workflow.\n* Extensible with custom operators.\n* High performance serving powered by [BentoML](https://github.com/bentoml/BentoML)\n\n## Supported Platforms:\n\n* [AWS Lambda](https://github.com/bentoml/aws-lambda-deploy)\n* [AWS SageMaker](https://github.com/bentoml/aws-sagemaker-deploy)\n* [AWS EC2](https://github.com/bentoml/aws-ec2-deploy)\n* [Google Cloud Run](https://github.com/bentoml/google-cloud-run-deploy)\n* [Google Compute Engine](https://github.com/bentoml/google-compute-engine-deploy)\n* [Azure Functions](https://github.com/bentoml/azure-functions-deploy)\n* [Azure Container Instances](https://github.com/bentoml/azure-container-instances-deploy)\n* [Heroku](https://github.com/bentoml/heroku-deploy)\n* Looking for **Kubernetes**? Try out [Yatai: Model deployment at scale on Kubernetes](https://github.com/bentoml/Yatai).\n* **Customize deploy target** by creating bentoctl plugin from the [deployment operator template](https://github.com/bentoml/bentoctl-operator-template).\n\n**Upcoming:**\n* [Knative](https://github.com/bentoml/bentoctl/issues/79) (WIP)\n\n\n## Install bentoctl\n```bash\npip install --pre bentoctl\n```\n\n| 💡 bentoctl designed to work with BentoML version 1.0.0 and above. For BentoML 0.13 or below, you can use the `pre-v1.0` branch in the operator repositories and follow the instruction in the README. You can also check out the quickstart guide for 0.13 [here](./docs/013-deployment.md).\n\n\n\n\n## Next steps\n\n- [Quickstart Guide](./docs/quickstart.md) walks through a series of steps to deploy a bento to AWS Lambda as API server.\n- [Core Concepts](./docs/core-concepts.md) explains the core concepts in bentoctl.\n- [Operator List](./docs/operator-list.md) lists official operators and their current status.\n\n## Community\n\n- To report a bug or suggest a feature request, use [GitHub Issues](https://github.com/bentoml/bentoctl/issues/new/choose).\n- For other discussions, use [Github Discussions](https://github.com/bentoml/BentoML/discussions) under the [BentoML repo](https://github.com/bentoml/BentoML/)\n- To receive release announcements and get support, join us on [Slack](http://join.slack.bentoml.org).\n\n\n## Contributing\n\nThere are many ways to contribute to the project:\n\n- Create and share new operators. Use [deployment operator template](https://github.com/bentoml/bentoctl-operator-template) to get started.\n- If you have any feedback on the project, share it with the community in [Github Discussions](https://github.com/bentoml/BentoML/discussions) under the [BentoML repo](https://github.com/bentoml/BentoML/).\n- Report issues you\'re facing and "Thumbs up" on issues and feature requests that are relevant to you.\n- Investigate bugs and reviewing other developer\'s pull requests.\n',
    'author': 'bentoml.org',
    'author_email': 'contact@bentoml.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bentoml/bentoctl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
