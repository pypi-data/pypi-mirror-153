#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'mpcurses',
        version = '0.4.1',
        description = 'Mpcurses is an abstraction of the Python curses and multiprocessing libraries providing function execution and runtime visualization capabilities',
        long_description = '# mpcurses #\n[![GitHub Workflow Status](https://github.com/soda480/mpcurses/workflows/build/badge.svg)](https://github.com/soda480/mpcurses/actions)\n[![Code Coverage](https://codecov.io/gh/soda480/mpcurses/branch/master/graph/badge.svg)](https://codecov.io/gh/soda480/mpcurses)\n[![Code Grade](https://api.codiga.io/project/12270/status/svg)](https://app.codiga.io/public/project/12270/mpcurses/dashboard)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/mpcurses.svg)](https://badge.fury.io/py/mpcurses)\n[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)\n\nMpcurses is an abstraction of the Python curses and multiprocessing libraries providing function execution and runtime visualization capabilities at scale. It contains a simple API to enable any Python function to be executed across one or more background processes and includes built-in directives to visualize the functions execution on a terminal screen. \n\nThe mpcurses API allows for seamless integration since it does not require the target function to include additional context about curses or multiprocessing. The target function does need to implement logging since log messages are the primary means of inter-process communication between the background processes executing the function and the main process updating the curses screen on the terminal.\n\nThe main features are:\n\n* Execute a function across one or more concurrent processes\n* Queue execution to ensure a predefined number of processes are running\n* Visualize function execution on the terminal screen using curses\n* Define the screen layout using a Python dict\n* Leverage built-in directives to dynamically update the screen when events occur by analyzing log messages\n  * Keep numeric counts\n  * Update text values and colors\n  * Maintain visual indicators\n  * Display progress bars\n  * Display tables\n  * Display lists\n\n Refer to documentation here: https://soda480.github.io/mpcurses/\n\n Mpcurses is a subclass of `mpmq`, see [mpmq](https://pypi.org/project/mpmq/) for more information.\n\n### Installation ###\n```bash\npip install mpcurses\n```\n\n### Examples ###\n\nTo run the samples below you need to install the namegenerator module `pip install namegenerator`\n\n\nA simple example using mpcurses:\n\n```python\nfrom mpcurses import MPcurses\nimport namegenerator, time, logging\nlogger = logging.getLogger(__name__)\n\ndef do_something(*args):\n    for _ in range(0, 600):\n        logger.debug(f\'processing item "{namegenerator.gen()}"\')\n        time.sleep(.01)\n\nMPcurses(\n    function=do_something,\n    screen_layout={\n        \'display_item\': {\n            \'position\': (1, 1),\n            \'text\': \'Processing:\',\n            \'text_color\': 0,\n            \'color\': 14,\n            \'clear\': True,\n            \'regex\': r\'^processing item "(?P<value>.*)"$\'\n        }\n    }).execute()\n ```\n\nExecuting the code above results in the following:\n![example](https://raw.githubusercontent.com/soda480/mpcurses/master/docs/images/example.gif)\n\nTo scale execution of the function across multiple processes; we set the `process_data` parameter to a list whose total number of elements represent the number of processes to execute, and each list element represent the data to be passed to each respective process:\n\n```python\nfrom mpcurses import MPcurses\nimport namegenerator, time, logging\nlogger = logging.getLogger(__name__)\n\ndef do_something(*args):\n    group = args[0].get(\'group\', 0)\n    for _ in range(0, 600):\n        logger.debug(f\'processing item "[{group}]: {namegenerator.gen()}"\')\n        time.sleep(.01)\n\nMPcurses(\n    function=do_something,\n    process_data=[{\'group\': 1}, {\'group\': 2}, {\'group\': 3}],\n    screen_layout={\n        \'display_item\': {\n            \'position\': (1, 1),\n            \'color\': 14,\n            \'clear\': True,\n            \'regex\': r\'^processing item "(?P<value>.*)"$\',\n            \'table\': True\n        }\n    }).execute()\n```\n\nExecuting the code above results in the following:\n![example](https://raw.githubusercontent.com/soda480/mpcurses/master/docs/images/example-multi.gif)\n\nServeral [examples](https://github.com/soda480/mpcurses/tree/master/examples) are included to help introduce the mpcurses library. Note the functions contained in all the examples are Python functions that have no context about multiprocessing or curses, they simply perform a function on a given dataset. Mpcurses takes care of setting up the multiprocessing, configuring the curses screen and maintaining the thread-safe queues that are required for inter-process communication.\n\n#### [example1](https://github.com/soda480/mpcurses/blob/master/examples/example1.py)\nExecute a function that processes a list of random items. The screen maintains indicators showing the number of items that have been processed. Two lists are maintained displaying the items that had errors and warnings.\n![example1](https://raw.githubusercontent.com/soda480/mpcurses/master/docs/images/example1.gif)\n\n#### [example2](https://github.com/soda480/mpcurses/blob/master/examples/example2.py)\nExecute a function that processes a list of random items. Execution is scaled across three processes where each is responsible for processing items for a particular group. The screen maintains indicators displaying the items that had errors and warnings for each group.\n![example2](https://raw.githubusercontent.com/soda480/mpcurses/master/docs/images/example2.gif)\n\n#### [example3](https://github.com/soda480/mpcurses/blob/master/examples/example3.py)\nExecute a function that calculates prime numbers for a set range of integers. Execution is scaled across 10 different processes where each process computes the primes on a different set of numbers. For example, the first process computes primes for the set 1-10K, second process 10K-20K, third process 20K-30K, etc. The screen keeps track of the number of prime numbers encountered for each set and maintains a progress bar for each process.\n![example3](https://raw.githubusercontent.com/soda480/mpcurses/master/docs/images/example3.gif)\n\n#### Running the examples ####\n\nBuild the Docker image and run the Docker container using the instructions described in the [Development](#development) section. Run the example scripts within the container:\n\n```bash\npython examples/example#.py\n```\n\n### Projects using `mpcurses` ###\n\n* [edgexfoundry/sync-github-labels](https://github.com/edgexfoundry/cd-management/tree/git-label-sync) A script that synchronizes GitHub labels and milestones\n\n* [edgexfoundry/prune-github-tags](https://github.com/edgexfoundry/cd-management/tree/prune-github-tags) A script that prunes GitHub pre-release tags\n\n### Development ###\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\nmpcurses:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nmpcurses:latest \\\n/bin/bash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n\nNOTE: the commands above assume your working behind a http proxy, if that is not the case then the proxy arguments can be discared from both commands.\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'emilio.reyes@intel.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/mpcurses',
        project_urls = {},

        scripts = [],
        packages = ['mpcurses'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = ['mpmq==0.2.0'],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
