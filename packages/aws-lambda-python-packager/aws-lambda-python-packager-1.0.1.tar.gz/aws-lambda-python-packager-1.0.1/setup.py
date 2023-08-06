# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_lambda_python_packager']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp',
 'appdirs',
 'colorama>=0.4',
 'fsspec',
 'packaging',
 'requests',
 'toml>=0.10']

extras_require = \
{':platform_system == "Windows"': ['python-certifi-win32']}

entry_points = \
{'console_scripts': ['lambda-packager = aws_lambda_python_packager:main_cli']}

setup_kwargs = {
    'name': 'aws-lambda-python-packager',
    'version': '1.0.1',
    'description': 'Description',
    'long_description': "# AWS Lambda Python Packager\n\nAn alternate way to package Python functions for AWS Lambda. Works cross-platform and cross-architecture if binary packages are available for all packages.\n\n```shell\n$ lambda-packager -h\nusage: lambda-packager [-h] [--ignore-packages] [--update-pyproject]\n                       [--python-version PYTHON_VERSION] [--architecture {x86_64,arm64}]\n                       [--region REGION] [--verbose] [--zip-output [ZIP_OUTPUT]]\n                       [--compile-python] [--use-aws-pyarrow] [--strip-tests] [--strip-libraries]\n                       [--strip-python] [--strip-other] [--optimize-all]\n                       pyproject_path output_path\n\nAWS Lambda Python Packager\n\npositional arguments:\n  pyproject_path        Path to pyproject.toml\n  output_path           Path to output directory\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --ignore-packages     Ignore packages that are already present in the AWS Lambda Python runtime\n                        (default: False)\n  --update-pyproject    Update pyproject.toml with the ignored packages (ignored if not --ignore-\n                        packages) (default: False)\n  --python-version PYTHON_VERSION, -pyv PYTHON_VERSION\n                        Python version to target (default: 3.9)\n  --architecture {x86_64,arm64}, -a {x86_64,arm64}\n                        Architecture to target (default: x86_64)\n  --region REGION       AWS region to target (default: us-east-1)\n  --verbose, -v         Verbose output (may be specified multiple times) (default: 0)\n  --zip-output [ZIP_OUTPUT], -z [ZIP_OUTPUT]\n                        Output zip file in addition to directory (default: False)\n\nOptimization Options:\n  --compile-python      Compile the python bytecode (default: None)\n  --use-aws-pyarrow     Use AWS wrangler pyarrow (may result in smaller file size). Pulls from\n                        https://github.com/awslabs/aws-data-wrangler/releases/ until it finds a\n                        Lambda layer that includes the proper PyArrow version. (default: False)\n  --strip-tests         Strip tests from the package\n  --strip-libraries     Strip debugging symbols from libraries\n  --strip-python        Strip python scripts from the package (requires --compile-python) (note,\n                        may need to set an ENV variable of PYTHONOPTIMIZE=2) (default: False)\n  --strip-other         Strip other files from the package ('.pyx', '.pyi', '.pxi', '.pxd', '.c',\n                        '.h', '.cc')\n  --optimize-all, -O    Turns on all size optimizations (equivalent to --strip-tests --strip-\n                        libraries --ignore-packages --update-pyproject --strip-other). May be\n                        specified multiple times. Second time will also enable --compile-python\n                        --strip-python --use-aws-pyarrow (default: 0)\n\n```\n",
    'author': 'Daniel Sullivan',
    'author_email': 'mumblepins@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mumblepins/aws-lambda-python-packager/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
