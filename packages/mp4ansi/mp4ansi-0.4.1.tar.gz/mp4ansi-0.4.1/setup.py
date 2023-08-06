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
        name = 'mp4ansi',
        version = '0.4.1',
        description = 'A simple ANSI-based terminal emulator that provides multi-processing capabilities.',
        long_description = '# mp4ansi #\n[![GitHub Workflow Status](https://github.com/soda480/mp4ansi/workflows/build/badge.svg)](https://github.com/soda480/mp4ansi/actions)\n[![Code Coverage](https://codecov.io/gh/soda480/mp4ansi/branch/main/graph/badge.svg?token=6NTX6LSP7Q)](https://codecov.io/gh/soda480/mp4ansi)\n[![Code Grade](https://api.codiga.io/project/20694/status/svg)](https://app.codiga.io/public/project/20694/mp4ansi/dashboard)\n[![vulnerabilities](https://img.shields.io/badge/vulnerabilities-None-brightgreen)](https://pypi.org/project/bandit/)\n[![PyPI version](https://badge.fury.io/py/mp4ansi.svg)](https://badge.fury.io/py/mp4ansi)\n[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)\n\n\nA simple ANSI-based terminal that provides various capabilities for showing off and/or scaling out your programs execution. MP4ansi is an abstraction of multiprocessing that leverages both the Terminal and ProgressBar. See the [examples](https://github.com/soda480/mp4ansi/tree/master/examples) for more detail.\n\n## Installation ##\n```bash\npip install mp4ansi\n```\n\n## Examples ##\n\nVarious [examples](https://github.com/soda480/mp4ansi/tree/master/examples) are included to demonstrate the mp4ansi package. To run the examples, build the Docker image and run the Docker container using the instructions described in the [Development](#development) section.\n\n### `MP4ansi`\n\nMP4ansi will scale execution of a specified function across multiple background processes, where each process is mapped to specific line on the terminal. As the function executes its log messages will automatically be written to the respective line on the terminal. The number of processes along with the arguments to provide each process is specified as a list of dictionaries. The number of elements in the list will dictate the total number of processes to execute (as well as the number of lines in the terminal). The result of each function is written to the respective dictionary element and can be interogated upon completion. \n\nMP4ansi is a subclass of `mpmq`, see the [mpmq](https://pypi.org/project/mpmq/) for more information.\n\nHere is a simple example:\n\n```python\nfrom mp4ansi import MP4ansi\nimport random, names, logging\nlogger = logging.getLogger(__name__)\n\ndef do_work(*args):\n    total = random.randint(50, 100)\n    logger.debug(f\'processing total of {total}\')\n    for _ in range(total):\n        logger.debug(f\'processed {names.get_full_name()}\')\n    return total\n\ndef main():\n    process_data = [{} for item in range(8)]\n    print(\'Procesing names...\')\n    MP4ansi(function=do_work, process_data=process_data).execute()\n    print(f"Total names processed {sum([item[\'result\'] for item in process_data])}")\n\nif __name__ == \'__main__\':\n    main()\n```\n\nExecuting the code above ([example1](https://github.com/soda480/mp4ansi/tree/master/examples/example1.py)) results in the following:\n![example](https://raw.githubusercontent.com/soda480/mp4ansi/master/docs/images/example1.gif)\n\n**Note** the function being executed `do_work` has no context about multiprocessing or the terminal; it simply perform a function on a given dataset. MP4ansi takes care of setting up the multiprocessing, setting up the terminal, and maintaining the thread-safe queues that are required for inter-process communication.\n\nLet\'s update the example to add a custom identifer for each process and to show execution as a progress bar. To do this we need to provide additonal configuration via the optional `config` parameter. Configuration is supplied as a dictionary; `id_regex` instructs how to query for the identifer from the log messages. For the progress bar, we need to specify `total` and `count_regex` to instruct how to query for the total and for when to count that an item has been processed. The value for these settings are specified as regular expressions and will match the function log messages, thus we need to ensure our function has log statements for these. If each instance of your function executes on a static data range then you can specify total as an `int`, but in this example the data range is dynamic, i.e. each process will execute on varying data ranges.\n\n```python\nfrom mp4ansi import MP4ansi\nimport names, random, logging\nlogger = logging.getLogger(__name__)\n\ndef do_work(*args):\n    logger.debug(f\'processor is {names.get_last_name()}\')\n    total = random.randint(50, 125)\n    logger.debug(f\'processing total of {total}\')\n    for _ in range(total):\n        logger.debug(f\'processed {names.get_full_name()}\')\n    return total\n\ndef main():\n    process_data = [{} for item in range(8)]\n    config = {\n        \'id_regex\': r\'^processor is (?P<value>.*)$\',\n        \'progress_bar\': {\n            \'total\': r\'^processing total of (?P<value>\\d+)$\',\n            \'count_regex\': r\'^processed (?P<value>.*)$\',\n            \'progress_message\': \'Finished processing names\'}}\n    print(\'Procesing names...\')\n    MP4ansi(function=do_work, process_data=process_data, config=config).execute()\n    print(f"Total names processed {sum([item[\'result\'] for item in process_data])}")\n\nif __name__ == \'__main__\':\n    main()\n```\n\nExecuting the code above ([example2](https://github.com/soda480/mp4ansi/tree/master/examples/example2.py)) results in the following:\n![example](https://raw.githubusercontent.com/soda480/mp4ansi/master/docs/images/example2.gif)\n\n### `Terminal`\n\nThe package also exposes a `Terminal` class if you wish to consume the terminal capabilities without executing background processes. Here is an example for how to do that:\n```python\nfrom mp4ansi import Terminal\nfrom essential_generators import DocumentGenerator\nimport time, random\n\ndef main():\n    print(\'generating random sentences...\')\n    count = 15\n    docgen = DocumentGenerator()\n    terminal = Terminal(count)\n    terminal.write_lines()\n    terminal.hide_cursor()\n    for _ in range(800):\n        index = random.randint(0, count - 1)\n        terminal.write_line(index, docgen.sentence())\n        time.sleep(.01)\n    terminal.write_lines(force=True)\n    terminal.show_cursor()\n\nif __name__ == \'__main__\':\n    main()\n```\n\nExecuting the code above ([example5](https://github.com/soda480/mp4ansi/tree/master/examples/example5.py)) results in the following:\n![example](https://raw.githubusercontent.com/soda480/mp4ansi/master/docs/images/example5.gif)\n\n## Development ##\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\nmp4ansi:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nmp4ansi:latest \\\n/bin/bash\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
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
        author_email = 'soda480@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/mp4ansi',
        project_urls = {},

        scripts = [],
        packages = ['mp4ansi'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'mpmq==0.2.0',
            'cursor',
            'colorama',
            'progress1bar'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
