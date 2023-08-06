# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ins_nav']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'squaternion']

setup_kwargs = {
    'name': 'ins-nav',
    'version': '0.6.0',
    'description': 'A library to do inertial navigation',
    'long_description': '[![](https://raw.githubusercontent.com/MomsFriendlyRobotCompany/ins_nav/master/docs/pics/header.jpg)](https://github.com/MomsFriendlyRobotCompany/ins_nav)\n\n# ins_nav\n\n[![Actions Status](https://github.com/MomsFriendlyRobotCompany/ins_nav/workflows/pytest/badge.svg)](https://github.com/MomsFriendlyRobotCompany/ins_nav/actions)\n![PyPI - License](https://img.shields.io/pypi/l/ins_nav.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ins_nav.svg)\n![PyPI - Format](https://img.shields.io/pypi/format/ins_nav.svg)\n![PyPI](https://img.shields.io/pypi/v/ins_nav.svg)\n\n\nThis library is written independent of any specific IMU. The idea is you pass in the appropriate\nmeasurements and error terms from your IMU and get the desired output.\n\n**This is still under heavy development**\n\n# Install\n\nThe suggested way to install this is via the `pip` command as follows:\n\n```\npip install ins_nav\n```\n\n## Development\n\nTo submit git pulls, clone the repository and set it up as follows:\n\n```\ngit clone https://github.com/MomsFriendlyRobotCompany/ins_nav\ncd ins_nav\npoetry install\n```\n\n## Usage\n\n- `ins_nav.wgs84` contains a bunch of useful constants: semi-major axis, gravity, etc\n- `ins_nav.ahrs` creates an attitude and heading reference system (AHRS) using accelerometers, gyroscopes, and magnetometers\n- `TiltCompensatedCompass` contains the mathematics of an IMU with accelerometers, gyroscopes, and magnetometers\n- `ins_nav.transforms` has a bunch of reference frame conversions: `ecef2llh`, `llh2ecef`, etc\n\n## Transforms (in work)\n\n### Earth Centered Frames\n\n* [ECI: Earth-centered Inertial](https://en.wikipedia.org/wiki/Earth-centered_inertial) is an\ninertial frame where Newton\'s laws of motion apply. It has its origin at the center of the\nEarth with:\n    - x-axis in the direction of the vernal equinox\n    - z-axis is parallel to the rotation of the Earth\n    - y-axis completes the right-handed coordinate system\n* [ECEF: Earth-centered, Earth-fixed](https://en.wikipedia.org/wiki/ECEF) has the same origin\nas ECI, but rotates with the Earth and the x-axis points towards the zero/prime\nmeridian. The ECEF frame rotates at 7.2921E-5 rads/sec with respect to the ECI\nframe\n* [LLA(H): Latitude, Longitude, Altitude(Height)](tbd) is similar to the ECEF frame, but\nis the frame historically used for navigation\n\n### Navigation Frames\n\n* [ENU: East North Up](https://en.wikipedia.org/wiki/Axes_conventions#Ground_reference_frames:_ENU_and_NED)\na local navigation frame, where *up* and the z-axis align, but clockwise right turns\nare negative\n* [NED: North East Down](https://en.wikipedia.org/wiki/North_east_down) a local navigation\nframe, where *up* and the z-axis are opposite, but the direction of right (clockwise)\nturns are in the positive direction and is the standard vehicle roll-pitch-yaw frame\n\n\n\n# Other Good Navigation Libraries\n\n- [lat_lon_parser](https://pypi.org/project/lat-lon-parser/) allows you to convert between\nmeasurements formats like `-45 deg 12\' 36.0 sec`, `45.21 W`, and `-45.21` easily\n- [nvector](https://www.navlab.net/nvector) has a lot of capability\n- [navpy](https://github.com/NavPy/NavPy) appears to be simple grad student work but code is well referenced (BSD)\n- [navigation](https://github.com/ngfgrant/navigation) does GPS navigation and way\npoints\n\n# Todo\n\n- extended kalman filter\n- navigation equations\n- error model\n\n# Change Log\n\n| Date       | Version | Notes                   |\n|------------|---------|-------------------------|\n| 2020-03-28 | 0.6.0   | moved to [poetry](https://python-poetry.org/) |\n| 2019-07-05 | 0.5.1   | cleanup and new functions|\n| 2017-07-07 | 0.0.1   | init                     |\n\n\n# The MIT License (MIT)\n\n**Copyright (c) 2017 Kevin J. Walchko**\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of\nthis software and associated documentation files (the "Software"), to deal in\nthe Software without restriction, including without limitation the rights to\nuse, copy, modify, merge, publish, distribute, sublicense, and/or sell copies\nof the Software, and to permit persons to whom the Software is furnished to do\nso, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS\nFOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\nIN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN\nCONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n',
    'author': 'walchko',
    'author_email': 'walchko@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/ins_nav/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
