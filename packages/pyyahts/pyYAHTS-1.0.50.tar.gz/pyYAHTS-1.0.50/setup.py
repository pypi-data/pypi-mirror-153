# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyYAHTS']

package_data = \
{'': ['*']}

install_requires = \
['fpdf>=1.7.2,<2.0.0',
 'gTTS>=2.2.4,<3.0.0',
 'json2table>=1.1.5,<2.0.0',
 'networkx>=2.7.1,<3.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pyats[full]==22.1',
 'pyvis>=0.1.9,<0.2.0',
 'rich-click>=1.2.1,<2.0.0',
 'rich>=12.1.0,<13.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['pyYAHTS = pyYAHTS.script:run']}

setup_kwargs = {
    'name': 'pyyahts',
    'version': '1.0.50',
    'description': 'An implementation of Cisco pyATS',
    'long_description': '# pyYAHTS\nAn interpretation of pyATS\n\npyYAHTS is a dyanmic, on-demand, YAML-free / testbed.yaml free, implementation of pyATS. \n\nIt works with any IOS / IOS-XE / IOS-XR / NXOS device!\n\nThe results are Rich JSON printed to the screen\n\n## Requirements\npyYAHTS is an extension of pyATS, which is required, and only runs on Linux operating systems\n## Installation\n\n1. pip install pyYAHTS\n\n## Getting Started\n\npyYAHTS works on any Cisco OS IOS / IOS-XE / IOS-XR / NXOS\n\npyYAHTS requires the follow options be speficied at runtime:\n\n1. (Required) Hostname of the device - must exactly match the configured hostname\n2. (Required) Operating System - Either ios, iosxe, iosxr, or nxos\n3. (Required) Username\n4. (Required) Password\n5. (Required) Command - Either a pyATS Learn Function, such as ospf, or any supported pyATS Parsed CLI Show Command, such as "show ip interface brief"\n6. (Optional) Filetype - Creates an output file - \n\n    Supported filetpyes: JSON, YAML, HTML, Datatable HTML, Markdown, PDF, CSV\n\n7. (Optional) Email - 3 required fields if you want to e-mail the output with GMail\n\n    --from_email - Your GMail Address\n\n    --email_password - Your Gmail Password\n\n    --to_email - The recipients Email\n    \n![Help](images/help01.png)\n\nFor a list of supported Learn Functions please visit [Available Learn Functions](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models)\n\n![Available Learn Functions](/images/available_learn_functions.png)\n\nFor a list of supported Parsers please visit [Available Show Command Parsers](https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers)\n\n![Available Show Parsers](/images/available_show_parsers01.png)\n\nA sample of "Show IP Interface" Parsers for IOS-XE\n![IOS-XE Show IP Interface Sample](/images/available_show_parsers02.png)\n\n\n## Using pyYAHTS\n\nIn any virtual environment with pyATS installed pyYAHTS can be executed several ways\n\n1. Prompted Inputs\n\n```python\n(virtualenv)$ pyYAHTS\nHostname: dist-sw01\nOS (ios, iosxe, iosxr, nxos): nxos\nUsername: cisco\nPassword:\nCommand: ospf\n```\n\n2. Directly supplying options\n\n```python\n(virtualenv)$ pyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf\n```\n\n3. Mixing supplied options and prompted responses\n\n```python\n(virtualenv)$ pyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco\nCommand: ospf\n```\n\n## Creating Output files\n\nIf you include the optional --filetype flag you can create JSON and YAML files from the data \n\n```python\npyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf --filetype json\npyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf --filetype yaml\npyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf --filetype html\npyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf --filetype datatable\npyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf --filetype markdown\npyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf --filetype pdf\npyYAHTS --hostname dist-sw01 --os nxos --username cisco --password cisco --command ospf --filetype csv\n```\n\n## E-Mail Network State\n\nIf you include the optional E-Mail flags you can send the network state data using GMail \n\nYou will have to enable IMAP permissions on your GMail Account [Enable IMAP in GMail](https://support.google.com/mail/answer/7126229?hl=en#zippy=%2Cstep-check-that-imap-is-turned-on)\n\nYou may also have to enable support for [Less Secure Apps](https://support.google.com/accounts/answer/6010255?hl=en)\n\nThe three required flags to send an email are:\n\n--from_email - Your GMail Address\n\n--email_password - Your Gmail Password\n\n--to_email - The recipients Email\n\nAdditonally if you specify a filetype (--filetype) the output file will be automatically attached to the email\n## Help\n\npyYAHTS includes a handy Rich Click Help! Simple type:\n\n```python\n$ pyYAHTS --help\n```\n\n![More Help](images/help01.png)\n\n## Contact\n\nPlease reach out on Twitter [Twitter](https://twitter.com/john_capobianco) or open an issue if you hit any snags or have any questions!',
    'author': 'John Capobianco',
    'author_email': 'ptcapo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/automateyournetwork/pyYAHTS',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
