# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['h1st',
 'h1st.core',
 'h1st.exceptions',
 'h1st.h1flow',
 'h1st.h1flow.ui',
 'h1st.model',
 'h1st.model.ensemble',
 'h1st.model.kswe',
 'h1st.model.oracle',
 'h1st.model.repository',
 'h1st.model.repository.storage',
 'h1st.trust']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.19.1,<0.20.0',
 'lime>=0.2.0.1,<0.3.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'pyyaml>=6.0,<7.0',
 's3fs>=2022.1.0,<2023.0.0',
 'scikit-fuzzy>=0.4.2,<0.5.0',
 'scikit-learn>=0.24.0',
 'shap>=0.36.0',
 'tensorflow>=2.8.0,<3.0.0',
 'ulid-py>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'h1st',
    'version': '0.1.11',
    'description': 'Human-First AI (H1ST)',
    'long_description': '## Join the Human-First AI revolution\n_“We humans have .. insight that can then be mixed with powerful AI .. to help move society forward. Second, we also have to build trust directly into our technology .. And third, all of the technology we build must be inclusive and respectful to everyone.”_\n<br/>— Satya Nadella, Microsoft CEO\n\nAs trail-blazers in Industrial AI, our team at Arimo-Panasonic has found Satya Nadella‘s observations to be powerful and prescient. Many hard-won lessons from the field have led us to adopt this approach which we call Human-First AI (`H1st` AI). \n\nToday, we‘re excited to share these ideas and concrete implementation of `H1st` AI with you and the open-source data science community!\n\n## Learn the Key Concepts\nHuman-First AI (`H1st` AI) solves three critical challenges in real-world data science:\n\n1. __Industrial AI needs human insight:__ In so many important applications, there isn‘t enough data for ML. For example, last year‘s product‘s data does not apply to this year‘s new model. Or, equipment not yet shipped obviously have no data history to speak of. `H1st` combines human knowledge and any available data to enable intelligent systems, and companies can achieve earlier time-to-market.\n\n2. __Data scientists need human tools:__ Today‘s tools are to compete rather than to collaborate. When multiple data scientists work on the same project, they are effectively competing to see who can build the better model. `H1st` breaks a large modeling problem into smaller, easier parts. This allows true collaboration and high productivity, in ways similar to well-established software engineering methodology. \n\n3. __AI needs human trust:__ AI models can\'t be deployed when they lack user trust. AI increasingly face regulatory challenges. `H1st` supports model description and explanation at multiple layers, enabling transparent and trustworthy AI.\n\n\n## Get started\n`H1st` runs on Python 3.8 or above. Install with \n```\npip install --upgrade pip\npip3 install h1st\n```\nFor Windows, please use 64bit version and install [VS Build Tools](https://visualstudio.microsoft.com/downloads/) before installing H1st.\n\nStart by reading about our [philosophy](https://h1st.readthedocs.io/en/latest/manifesto/README.html) and [Object Model](https://h1st.readthedocs.io/en/latest/concepts/object-model.html)\n\nSee the [Quick Start](https://h1st.readthedocs.io/en/latest/tutorials/quick-start/README.html) for simple "Hello world" examples of using [H1st rule-based model](https://h1st.readthedocs.io/en/latest/tutorials/quick-start/README.html#rule-based-model) & [H1st ML model](https://h1st.readthedocs.io/en/latest/tutorials/quick-start/README.html#mlmodeler-and-mlmodel) and using [H1st Graph](https://h1st.readthedocs.io/en/latest/tutorials/quick-start/README.html#h1st-graph).\n\n\n## Read the Documentation, Tutorials, and API Documentation\n\nGo over [the Concepts](https://h1st.readthedocs.io/en/latest/concepts/README.html)\n\nFor a simple real-world data science example using H1st Modeler and Model API, take a look at\n- [Modeler and Model with Iris dataset](https://h1st.readthedocs.io/en/latest/tutorials/examples/modeler-model.html).\n- [H1st Oracle: Combine Encoded Domain Knowledge with Machine Learning](https://h1st.readthedocs.io/en/latest/tutorials/examples/oracle-iot.html) in which we used Microsoft Azure Predictive Maintenance dataset to demonstrate the power of the Oracle.\n\nTo fully understand H1st philosophy and power, check out the [Use-case examples](https://h1st.readthedocs.io/en/latest/tutorials/use-cases/README.html).\n\nFor a deep dive into the components, please refer to our full [API Documentation](https://h1st.readthedocs.io/en/latest/api/README.html).\n\n## Join and Learn from Our Open-Source Community\nWe are collaborating with the open-source community. For Arimo-Panasonic, use cases include industrial applications such as Cybersecurity, Predictive Maintenance, Fault Prediction, Home Automation, Avionic & Automotive Experience Management, etc.\n\nWe\'d love to see your use cases and your contributions to open-source `H1st` AI. \n',
    'author': 'h1st-ai',
    'author_email': 'engineering@aitomatic.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://h1st.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
