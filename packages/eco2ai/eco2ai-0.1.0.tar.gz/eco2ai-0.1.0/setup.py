# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eco2ai', 'eco2ai.tools']

package_data = \
{'': ['*'], 'eco2ai': ['data/*']}

install_requires = \
['APScheduler>=3.8.1,<4.0.0',
 'numpy>=1.22.1,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'psutil>=5.9.0,<6.0.0',
 'py-cpuinfo>=8.0.0,<9.0.0',
 'pynvml>=11.4.1,<12.0.0',
 'requests>=2.27.1,<3.0.0',
 'tzlocal>=4.1,<5.0']

setup_kwargs = {
    'name': 'eco2ai',
    'version': '0.1.0',
    'description': 'emission tracking library',
    'long_description': '# Eco2AI\n\nEco2AI - is a python library which calculates power consumption and CO2 emission during running code.\nEmission information is written to file. Every single run of tracker creates line in this file with following items:\n\n+ project_name\n+ experiment_description\n+ start_time\n+ duration(s)\n+ power_consumption(kWTh)\n+ CO2_emissions(kg)\n+ CPU_name\n+ GPU_name\n+ OS\n+ country\n\n##  Installation\nTo install eco2ai library run next command:\n\n```\npip install eco2ai\n```\n\n## Use examples\n\neco2ai\'s interface is quite simple. Here is a the most straightforward usage example:\n```python\n\nimport eco2ai\n\ntracker = eco2ai.Tracker(project_name="YourProjectName", experiment_description="training the <your model> model")\n\ntracker.start()\n\n<your gpu &(or) cpu calculations>\n\ntracker.stop()\n```\n\neco2ai also supports decorators. Once decorated function executed, emissions info will be written to the file. See example below:\n```python\nfrom eco2ai import track\n\n@track\ndef train_func(model, dataset, optimizer, epochs):\n    ...\n\ntrain_func(your_model, your_dataset, your_optimizer, your_epochs)\n```\n\n\nFor your convenience every time you initilize a Tracker object with your custom parameters, this settings will be saved until library is uninstalled, and then every new tracker will be created with your custom settings(if you will create new tracker with new parameters, then they will be saved instead of old ones). For example:\n\n```python\n\nimport eco2ai\n\ntracker = eco2ai.Tracker(\n    project_name="YourProjectName", \n    experiment_description="training <your model> model",\n    file_name="emission.csv"\n    )\n\ntracker.start()\n<your gpu &(or) cpu calculations>\ntracker.stop()\n\n...\n\n# now, we want to create a new tracker for new calculations\ntracker = eco2ai.Tracker()\n# now, it\'s equivelent to:\n# tracker = eco2ai.Tracker(\n#     project_name="YourProjectName", \n#     experiment_description="training the <your model> model",\n#     file_name="emission.csv"\n# )\ntracker.start()\n<your gpu &(or) cpu calculations>\ntracker.stop()\n\n```\n\nYou can also set parameters using set_params() function, like in the example below:\n\n```python\nfrom eco2ai import set_params, Tracker\n\nset_params(\n    project_name="My_default_project_name",\n    experiment_description="We trained...",\n    file_name="my_emission_file.csv"\n)\n\ntracker = Tracker()\n# now, it\'s equivelent to:\n# tracker = Tracker(\n#     project_name="My_default_project_name",\n#     experiment_description="We trained...",\n#     file_name="my_emission_file.csv"\n# )\ntracker.start()\n<your code>\ntracker.stop()\n```\n\n\n\n<!-- There is [sber_emission_tracker_guide.ipynb](https://github.com/vladimir-laz/AIRIEmisisonTracker/blob/704ff88468f6ad403d69a63738888e1a3c41f59b/guide/sber_emission_tracker_guide.ipynb)  - useful jupyter notebook with more examples and notes. We highly recommend to check it out beforehand. -->\n## Important note\nIn order to calculate gpu & cpu power consumption correctly you should create the \'Tracker\' before any gpu or cpu usage\n\nFor every new calculation create a new “Tracker.”\n\n# Feedback\nIf you had some problems while working with our tracker, please, give us a feedback comments in [document](https://docs.google.com/spreadsheets/d/1927TwoFaW7R_IFC6-4xKG_sjlPUaYCX9vLqzrOsASB4/edit#gid=0)\n',
    'author': 'AI Lab, Sber',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sb-ai-lab/Eco2AI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
