# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['netbox_giftwrap']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'gTTS>=2.2.4,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich-click>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['netbox_giftwrap = netbox_giftwrap.script:run']}

setup_kwargs = {
    'name': 'netbox-giftwrap',
    'version': '1.0.0',
    'description': 'Transform NetBox APIs into Business Ready Documents',
    'long_description': '![Logo](/images/netbox_giftwrap.png)\n# netbox_giftwrap\nTransform NetBox APIs into Business Ready formats\n\n## Installing netbox_giftwrap\nTo install netbox_giftwrap there are a few simple steps:\n#### Ubuntu Linux \n##### The following instructions are based on Windows WSL2 and Ubuntu however any flavour of Linux will work with possibly slightly different commands.\n\n##### Confirm Python 3 is installed\n\n#####\n```console\n\n$ python3 -V\nPython 3.9.10\n\n```\n\n##### Create and activate a virtual environment\n\n######\n```console\n\n$ sudo apt install python3-venv\n$ python3 -m venv netbox_giftwrap\n$ source netbox_giftwrap/bin/activate\n(netbox_giftwrap)$\n\n```\n##### Install the netbox_giftwrap\n```console\n\n(netbox_giftwrap)$pip install netbox_giftwrap\n\n```\n\n##### Create an output folder\n```console\n\n(netbox_giftwrap)$mkdir output\n\n```\n### Windows\n\n#### [Download Python](https://python.org)\n#### Create and activate a virtual environment\n#####\n```console\n\nC:\\>python3 -m venv netbox_giftwrap\nC:\\>netbox_giftwrap\\Scripts\\activate\n(netbox_giftwrap) C:\\>\n\n```\n#### Install netbox_giftwrap\n```console\n\n(message_room)$pip install netbox_giftwrap\n\n```\n\n##### Create an output folder\n```console\n\n(netbox_giftwrap)$mkdir output\n\n```\n## Using the bot\n### Run the bot as an interactive session\n```console\n\n(netbox_giftwrap)$ cd output\n(netbox_giftwrap)$~/output/netbox_giftwrap.py\n\n```\n\n### The form questions:\n\n##### Question 1 - NetBox URL:\n\nEnter the URL of your NetBox instance (e.g. https://demo.netbox.dev):\n\nThis can be set as an environment variable\n\n##### Question 2 - NetBox API Token: \n\nEnter your NetBox API Token - you can create / retrieve one from https://URL/user/api-tokens/\n\nThis can be set as an environment variable\n\n##### Question 3 - NetBox API:\n\nThe NetBox API you want to transform.\n\nYou can use "?" to list all available APIs.\n\nYou can use "all" to transform all available APIs.\n\nThe list of currently available APIs:\n\naggregates\nasns\ncables\ncircuit-terminations\ncircuit-types\ncircuits\ncluster-groups\ncluster-types\nclusters\nconsole-port-templates\nconsole-ports\ncontact-assignments\ncontact-groups\ncontact-roles\ncontacts\ndevice-bay-templates\ndevice-bays\ndevice-roles\ndevice-types\ndevices\nfront-port-templates\nfront-ports\ngroups\ninterface-templates\ninterfaces\ninventory-items\nip-addresses\nip-ranges\nlocations\nmanufacturers\nmodule-bay-templates\nmodule-bays\nmodule-types\nmodules\nplatforms\npower-feeds\npower-outlet-templates\npower-outlets\npower-panels\npower-port-templates\npower-ports\nprefixes\nprovider-networks\nproviders\nrack-reservations\nrack-roles\nracks\nrear-port-templates\nrear-ports\nregions\nrirs\nroles\nroute-targets\nservice-templates\nservices\nsite-groups\nsites\nstatus\ntenant-groups\ntenants\ntokens\nusers\nvirtual-chassis\nvirtual-interfaces\nvirtual-machines\nvlan-groups\nvlans\n\n##### Question 4 - Filetype Filetype (none, json, yaml, html, csv, markdown, mindmap, mp3, all)[none]:\n\nIf you do not select a filetype the NetBox API JSON will print to the screen.\n\nYou can select "all" to transform the NetBox API into all available filetypes.\n\nThe MindMaps require the VS Code markmap extension to render them inside the IDE.\n\nIt is recommended to use Excel Preview VS Code extension to preview the CSV output files. \n\nMindmap and MP3 generate 1 file-per result. ',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
