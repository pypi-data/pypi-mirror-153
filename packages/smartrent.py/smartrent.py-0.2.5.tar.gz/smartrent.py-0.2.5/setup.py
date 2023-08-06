# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smartrent']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'websockets>=10.1,<11.0']

setup_kwargs = {
    'name': 'smartrent.py',
    'version': '0.2.5',
    'description': 'Unofficial Python API for SmartRent devices',
    'long_description': "# SmartRent API\n\n[![PyPI version][pypi-version-badge]](https://pypi.org/project/smartrent-py/)\n[![Supported Python versions][supported-versions-badge]](https://pypi.org/project/smartrent-py/)\n[![PyPI downloads monthly][m-downloads-badge]](https://pypistats.org/packages/smartrent-py)\n[![GitHub License][license-badge]](LICENSE.txt)\n[![Documentation Status][docs-badge]](https://smartrentpy.readthedocs.io/en/latest/?badge=latest)\n[![Code style: black][black-badge]](https://github.com/psf/black)\n\nUnofficial api for SmartRent devices\n\nUses websockets for communication and supports async functions\n\nFeel free to ⭐️ this repo to get notified about the latest features!\n\n[📚 Read the docs! 📚](https://smartrentpy.readthedocs.io)\n## Supported Devices\nThis client supports:\n* 🔐 Door Locks\n* 🌡 Thermostats\n* 💧 Leak Sensors\n* 💡 Binary Switches\n\n\n## Usage\n\n### Installation\n\n```bash\npip install smartrent.py\n```\n\n### Getting an API Object\nIn order to get an api object to interact with, you must login with the `async_login` function. This starts and handles a web session with SmartRent.\n\n```python\nimport asyncio\n\nfrom smartrent import async_login\n\nasync def main():\n    api = await async_login('<EMAIL>', '<PASSWORD>')\n\nasyncio.run(main())\n```\n\n### Getting Devices\nYou can get lists of your devices from the api with the `get_locks`, `get_thermostats`, `get_switches` and `get_leak_sensors` functions. You can then interact with the devices with their getter and setter functions.\n\n```python\nimport asyncio\n\nfrom smartrent import async_login\n\nasync def main():\n    api = await async_login('<EMAIL>', '<PASSWORD>')\n\n    lock = api.get_locks()[0]\n    locked = lock.get_locked()\n\n    if not locked:\n        await lock.async_set_locked(True)\n\nasyncio.run(main())\n```\n\n### Automatic Updating\nIf you need to get live updates to your device object from SmartRent, you can do that by calling `start_updater`. You can stop getting updates by calling `stop_updater`.\n\nYou can also set a callback function via `set_update_callback` that will be called when an update is triggered.\n\nFor example, if you want to set your thermostat to `Dad Mode` you can trigger an event every time the `cooling_setpoint` is changed and just change it back to your own desired value.\n```python\nimport asyncio\n\nfrom smartrent import async_login\n\nasync def main():\n    api = await async_login('<EMAIL>', '<PASSWORD>')\n\n    thermo = api.get_thermostats()[0]\n    thermo.start_updater()\n\n    CONSTANT_COOL = 80\n\n    async def on_evt():\n        if CONSTANT_COOL != thermo.get_cooling_setpoint():\n            await thermo.async_set_cooling_setpoint(CONSTANT_COOL)\n\n    thermo.set_update_callback(on_evt)\n\n    while True:\n        await asyncio.sleep(60)\n\nasyncio.run(main())\n```\n\n## Development\n### Setting up dev enviornment\n\n```\npip install -r requirements_test.txt\n```\n\n### Running the code formatter\n[Black](https://github.com/psf/black) is used for quick and easy code formatting\n\n```\nblack smartrent\n```\n\n## Special thanks\nMuch inspiration was taken from these projects:\n\n[AMcPherran/SmartRent-MQTT-Bridge](https://github.com/AMcPherran/SmartRent-MQTT-Bridge)\n\n[natanweinberger/smartrent-python](https://github.com/natanweinberger/smartrent-python)\n\n[Burry/homebridge-smartrent](https://github.com/Burry/homebridge-smartrent)\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).\n\n# TODOs\n\n* Add support for Two Factor Auth\n\n[pypi-version-badge]: https://img.shields.io/pypi/v/smartrent-py.svg?logo=pypi&logoColor=FFE873&style=for-the-badge\n[supported-versions-badge]: https://img.shields.io/pypi/pyversions/smartrent-py.svg?logo=python&logoColor=FFE873&style=for-the-badge\n[downloads-badge]: https://static.pepy.tech/personalized-badge/smartrent-py?period=total&units=international_system&left_color=grey&right_color=orange&left_text=total%20downloads&style=for-the-badge\n[m-downloads-badge]: https://img.shields.io/pypi/dm/smartrent-py.svg?style=for-the-badge\n[license-badge]: https://img.shields.io/github/license/ZacheryThomas/smartrent.py.svg?style=for-the-badge\n[docs-badge]: https://readthedocs.org/projects/smartrentpy/badge/?version=latest&style=for-the-badge\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge\n",
    'author': 'Zachery Thomas',
    'author_email': 'zacherythomas12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zacherythomas/smartrent.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
