# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbox',
 'nbox.framework',
 'nbox.hyperloop',
 'nbox.lib',
 'nbox.nbxlib',
 'nbox.sub_utils']

package_data = \
{'': ['*'], 'nbox': ['assets/*'], 'nbox.framework': ['protos/*']}

install_requires = \
['Jinja2==3.0.3',
 'dill==0.3.4',
 'grpcio==1.43.0',
 'mypy-protobuf==3.2.0',
 'protobuf==4.21.1',
 'python-json-logger==2.0.2',
 'randomname>=0.1.3,<0.2.0',
 'requests>=2.25.1,<3.0.0',
 'tabulate==0.8.9']

setup_kwargs = {
    'name': 'nbox',
    'version': '0.9.12',
    'description': 'ML Inference 🥶',
    'long_description': '<a href="https://nimblebox.ai/" target="_blank"><img src="./assets/built_at_nbx.svg" align="right"></a>\n\n# 🏖️ Nbox\n\n`nbox` is NimbleBox.ai\'s official SDK.\n\n> The entire purpose of this package is to make using ML 🥶.\n\n```\npip install nbox\n```\n\n## 🔥 Usage\n\n`nbox` provides first class support API for all NimbleBox.ai infrastructure (NBX-Build, Jobs, Deploy) and services (NBX-Workspaces) components. Write jobs using `nbox.Operators`:\n\n```python\nfrom nbox import Operator\nfrom nbox.nbxlib.ops import Magic\n\n# define a class object\nweekly_trainer: Operator = Magic()\n\n# call your operators\nweekly_trainer(\n  pass_values = "directly",\n)\n\n# confident? deploy it to your cloud\nweekly_trainer.deploy(\n  job_id_or_name = "magic_jobs",\n  schedule = Schedule(4, 30, [\'fri\']) # schedule like humans\n)\n```\n\nDeploy your machine learning or statistical models:\n\n```python\nfrom nbox import Model\nfrom transformers import AutoModelForSequenceClassification, AutoTokenizer\n\n# define your pre and post processing functions\ndef pre(x: Dict):\n  return AutoTokenizer(**x)\n\n# load your classifier with functions\nmodel = AutoModelForSequenceClassification.from_pretrained("distill-bert")\nclassifier = Model(model, pre = pre)\n\n# call your model\nclassifier(f"Is this a good picture?")\n\n# get full control on exporting it\nspec = classifier.torch_to_onnx(\n  TorchToOnnx(...)\n)\n\n# confident? deploy it your cloud\nurl, key = classifier.deploy(\n  spec, deployment_id_or_name = "classification"\n)\n\n# use it anywhere\npred = requests.post(\n  url,\n  json = {\n    "text": f"Is this a good picture?"\n  },\n  header = {"Authorization": f"Bearer {key}"}\n).json()\n```\n\n# 🧩 License\n\nThe code in thist repo is licensed as [Apache License 2.0](./LICENSE). Please check for individual repositories for licenses.\n',
    'author': 'NBX Research',
    'author_email': 'research@nimblebox.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NimbleBoxAI/nbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
