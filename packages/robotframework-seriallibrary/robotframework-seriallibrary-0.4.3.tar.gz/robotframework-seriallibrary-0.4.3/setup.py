# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['SerialLibrary']

package_data = \
{'': ['*']}

install_requires = \
['install_requires', 'install_requires']

setup_kwargs = {
    'name': 'robotframework-seriallibrary',
    'version': '0.4.3',
    'description': 'Robot Framework test library for serial connection',
    'long_description': '====================================\nSerialLibrary for Robot Framework\n====================================\n\nThis is a serial port test library for Robot Framework.\n\n\nExample::\n\n    *** settings ***\n    Library    SerialLibrary    loop://    encoding=ascii\n\n    *** test cases ***\n    Hello serial test\n         Write Data    Hello World\n         Read Data Should Be    Hello World\n\n\nAnother Example::\n\n    *** settings ***\n    Library    SerialLibrary\n\n    *** test cases ***\n    Read Until should read until terminator or size\n        [Setup]    Add Port    loop://    timeout=0.1\n        ${bytes} =    Set Variable    \n        Write Data    01 23 45 0A 67 89 AB CD EF\n        ${read} =    Read Until\n        Should Be Equal As Strings    ${read}    01 23 45 0A\n        ${read} =    Read Until   size=2\n        Should Be Equal As Strings    ${read}    67 89\n        ${read} =    Read Until   terminator=CD\n        Should Be Equal As Strings    ${read}    AB CD\n        ${read} =    Read Until\n        Should Be Equal As Strings    ${read}    EF\n        ${read} =    Read Until\n        Should Be Equal As Strings    ${read}    ${EMPTY}\n        [Teardown]    Delete All Ports\n',
    'author': 'Yasushi Masuda',
    'author_email': 'whosaysni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whosaysni/robotframework-seriallibrary/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
