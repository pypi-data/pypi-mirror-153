# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvjoystick']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyvjoystick',
    'version': '1.0.0',
    'description': 'Python bindings for vJoy',
    'long_description': '# pyvjoystick\n\npyvjoystick is a set of python binding for <a href=\'https://sourceforge.net/projects/vjoystick/\'>vJoy</a>(on github from <a href=\'https://github.com/jshafer817/vJoy\'>jshafer817</a> and <a href=\'https://github.com/njz3/vJoy/\'>njz3</a>). This repository is based off <a href="https://github.com/tidzo/pyvjoy">tidzo</a>\'s package.\n\n\nI will extend the support for others vJoysticks like ScpVBus.\n### Requirements\n\nInstall vJoy from <a href=\'https://sourceforge.net/projects/vjoystick/\'>sourceforge</a> or <a href=\'https://github.com/njz3/vJoy/\'>github</a>. It is recommended to also install the vJoy Monitor and Configure vJoy programs. These should be an option during installation.\n\n\n### Installation\n\nSimple! This package is installable by pip\n\n`pip install pyvjoystick`\n\n\n### Usage\n\nWith this library you can easily set Axis and Button values on any vJoy device. Low-level bindings are provided in `pyvjoy._sdk`.\n\n```python\nimport pyvjoy\n\n#Pythonic API, item-at-a-time\nj = pyvjoy.VJoyDevice(1)\n\n#turn button number 15 on\nj.set_button(15,1)\n\n#Notice the args are (buttonID,state) whereas vJoy\'s native API is the other way around.\n\n\n#turn button 15 off again\nj.set_button(15,0)\n\n#Set X axis to fully left\nj.set_axis(pyvjoy.HID_USAGE_X, 0x1)\n\n#Set X axis to fully right\nj.set_axis(pyvjoy.HID_USAGE_X, 0x8000)\n\n#Also implemented:\n\nj.reset()\nj.reset_buttons()\nj.reset_povs()\n\n\n#The \'efficient\' method as described in vJoy\'s docs - set multiple values at once\n\nj.data\n>>> <pyvjoy._sdk._JOYSTICK_POSITION_V2 at 0x....>\n\n\nj.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)\nj.data.wAxisX = 0x2000 \nj.data.wAxisY= 0x7500\n\n#send data to vJoy device\nj.update()\n\n\n#Lower-level API just wraps the functions in the DLL as thinly as possible, with some attempt to raise exceptions instead of return codes.\n```',
    'author': 'fsadannn',
    'author_email': 'fsadannn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fsadannn/pyvjoy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
