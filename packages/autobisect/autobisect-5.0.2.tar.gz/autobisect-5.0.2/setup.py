# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autobisect',
 'autobisect.evaluators',
 'autobisect.evaluators.browser',
 'autobisect.evaluators.browser.tests',
 'autobisect.evaluators.js',
 'autobisect.tests']

package_data = \
{'': ['*'],
 'autobisect.tests': ['mock-firefoxci/api/index/v1/task/*',
                      'mock-firefoxci/api/queue/v1/task/BfFeMY14Qyu_rMA2pxfZZg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/BfFeMY14Qyu_rMA2pxfZZg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/DYaFBxzITgCwBUp48Bugtw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/DYaFBxzITgCwBUp48Bugtw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/EYhOnvRFQd-rMlW2oAl10A/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/EYhOnvRFQd-rMlW2oAl10A/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/FnPonlT1QVSw-B0M0KcotQ/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/FnPonlT1QVSw-B0M0KcotQ/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/H5Dl5ijpSpOPwMLEEWx_bA/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/H5Dl5ijpSpOPwMLEEWx_bA/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HFsFsbogQ0O-sFZoYDmAZw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HFsFsbogQ0O-sFZoYDmAZw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HNaxi6w_RQeXGb4fYQFtwA/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HNaxi6w_RQeXGb4fYQFtwA/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HPE2LlTUQU62unXX8GvNGA/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HPE2LlTUQU62unXX8GvNGA/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/HX3oSg_SRTq5-Mc5D0PPHg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/HX3oSg_SRTq5-Mc5D0PPHg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/Hq2DMUk6QP26axMV8fDi9w/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/Hq2DMUk6QP26axMV8fDi9w/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/JucwusRxQHKQwDUPoOJIhQ/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/JucwusRxQHKQwDUPoOJIhQ/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/NKFp2FPpQ06E8C7N30JPdw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/NKFp2FPpQ06E8C7N30JPdw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/O1Sh28LhQC62SfLAi0orxg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/O1Sh28LhQC62SfLAi0orxg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/R2zRDt-ATf-zE-hYXR8kEw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/R2zRDt-ATf-zE-hYXR8kEw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/SDAzDRggRPOPYHEQC4WDEw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/SDAzDRggRPOPYHEQC4WDEw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/Tp5LesydQWyPNqpMThZLyg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/Tp5LesydQWyPNqpMThZLyg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/TxMd0rIfQKucR6p0gkaMSw/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/TxMd0rIfQKucR6p0gkaMSw/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/UXVT--1qQfeaGtNICDKx3w/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/UXVT--1qQfeaGtNICDKx3w/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/WLcjhVjtTLW0A_ued1Io-Q/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/WLcjhVjtTLW0A_ued1Io-Q/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/YDdWsEINSIyrct5ZV_nGzQ/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/YDdWsEINSIyrct5ZV_nGzQ/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/Zb_1byPDSTyhUkZeCg-PZg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/Zb_1byPDSTyhUkZeCg-PZg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/cRT3ROAzReG2wv7PW08JMg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/cRT3ROAzReG2wv7PW08JMg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/cSP0vuVWTX6JspZ2VTtDdg/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/cSP0vuVWTX6JspZ2VTtDdg/artifacts/public/build/*',
                      'mock-firefoxci/api/queue/v1/task/fXYHDLC_RkWNtOv01aB8wQ/artifacts/*',
                      'mock-firefoxci/api/queue/v1/task/fXYHDLC_RkWNtOv01aB8wQ/artifacts/public/build/*',
                      'mock-hg/mozilla-central/*']}

install_requires = \
['fuzzfetch>=2.0.0,<3.0.0',
 'grizzly-framework>=0.14.0,<0.15.0',
 'lithium-reducer>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['autobisect = autobisect.main:main']}

setup_kwargs = {
    'name': 'autobisect',
    'version': '5.0.2',
    'description': 'Automatic bisection utility for Mozilla Firefox and SpiderMonkey',
    'long_description': 'Autobisect\n==========\n[![Task Status](https://community-tc.services.mozilla.com/api/github/v1/repository/MozillaSecurity/autobisect/master/badge.svg)](https://community-tc.services.mozilla.com/api/github/v1/repository/MozillaSecurity/autobisect/master/latest)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/MozillaSecurity/autobisect/branch/master/graph/badge.svg)](https://codecov.io/gh/MozillaSecurity/autobisect)\n\nAutobisect is a python module that automates bisection of Mozilla Firefox and SpiderMonkey bugs.\n\nInstallation\n------------\n\n```bash\ngit clone git@github.com:MozillaSecurity/autobisect.git\ncd autobisect\npoetry install\n```\n\nUsage\n-----\nFirefox bug bisection supports the following arguments:\n\n```\npython -m autobisect firefox --help\nusage: __main__.py firefox [-h] [--log-level LOG_LEVEL] [--start START] [--end END] [--timeout TIMEOUT] [--repeat REPEAT] [--config CONFIG] [--find-fix] [--os {Android,Darwin,Linux,Windows}]\n                           [--cpu {AMD64,ARM64,aarch64,arm,arm64,i686,x64,x86,x86_64}] [--central | --release | --beta | --esr-stable | --esr-next | --try | --autoland] [-d] [-a] [-t] [--fuzzing]\n                           [--fuzzilli] [--coverage] [--valgrind] [--no-opt] [--launch-timeout LAUNCH_TIMEOUT] [-p PREFS] [--xvfb] [--ignore [IGNORE [IGNORE ...]]]\n                           testcase\n\npositional arguments:\n  testcase              Path to testcase\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --log-level LOG_LEVEL\n                        Configure console logging. Options: DEBUG, INFO, WARN, ERROR, CRIT (default: INFO)\n\nBoundary Arguments:\n  Accepts revision or build date in YYYY-MM-DD format)\n\n  --start START         Start build id (default: earliest available build)\n  --end END             End build id (default: latest available build)\n\nBisection Arguments:\n  --timeout TIMEOUT     Maximum iteration time in seconds (default: 60)\n  --repeat REPEAT       Number of times to evaluate testcase (per build)\n  --config CONFIG       Path to optional config file\n  --find-fix            Identify fix date\n\nTarget Arguments:\n  --os {Android,Darwin,Linux,Windows}\n                        Specify the target system. (default: Linux)\n  --cpu {AMD64,ARM64,aarch64,arm,arm64,i686,x64,x86,x86_64}\n                        Specify the target CPU. (default: x86_64)\n\nBranch Arguments:\n  --central             Download from mozilla-central (default)\n  --release             Download from mozilla-release\n  --beta                Download from mozilla-beta\n  --esr-stable          Download from esr-stable\n  --esr-next            Download from esr-next\n  --try                 Download from try\n  --autoland            Download from autoland\n\nBuild Arguments:\n  -d, --debug           Get debug builds w/ symbols (default=optimized).\n  -a, --asan            Download AddressSanitizer builds.\n  -t, --tsan            Download ThreadSanitizer builds.\n  --fuzzing             Download --enable-fuzzing builds.\n  --fuzzilli            Download --enable-js-fuzzilli builds.\n  --coverage            Download --coverage builds.\n  --valgrind            Download Valgrind builds.\n  --no-opt              Download non-optimized builds.\n\nLauncher Arguments:\n  --launch-timeout LAUNCH_TIMEOUT\n                        Number of seconds to wait before LaunchError is raised (default: 300)\n  -p PREFS, --prefs PREFS\n                        Optional prefs.js file to use\n  --xvfb                Use Xvfb (Linux only)\n\nReporter Arguments:\n  --ignore [IGNORE [IGNORE ...]]\n                        Space separated list of issue types to ignore. Valid options: log-limit memory timeout (default: log-limit memory timeout)\n```\n\nSimple Bisection\n----------------\n```\npython -m autobisect firefox trigger.html --prefs prefs.js --asan --end 2017-11-14\n```\n\nBy default, Autobisect will cache downloaded builds (up to 30GBs) to reduce bisection time.  This behavior can be modified by supplying a custom configuration file in the following format:\n```\n[autobisect]\nstorage-path: /home/ubuntu/cached\npersist: true\n; size in MBs\npersist-limit: 30000\n```\n\nDevelopment\n-----------\nAutobisect includes a pre-commit hook for [black](https://github.com/psf/black) and [flake8](https://flake8.pycqa.org/en/latest/).  To install the pre-commit hook, run the following.  \n```bash\npre-commit install\n```\n\nFurthermore, all tests should be executed via tox.\n```bash\npoetry run tox\n```\n\n',
    'author': 'Jason Kratzer',
    'author_email': 'jkratzer@mozilla.com',
    'maintainer': 'Mozilla Fuzzing Team',
    'maintainer_email': 'fuzzing@mozilla.com',
    'url': 'https://github.com/MozillaSecurity/autobisect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
