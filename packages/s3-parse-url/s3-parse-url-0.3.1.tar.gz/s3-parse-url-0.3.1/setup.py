# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s3_parse_url', 's3_parse_url.ext', 's3_parse_url.storages']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 's3-parse-url',
    'version': '0.3.1',
    'description': 'A small tool to parse URLs for S3 compatible storage services',
    'long_description': '############\ns3-parse-url\n############\n\n.. image:: https://img.shields.io/pypi/pyversions/s3-parse-url\n  :alt: PyPI - Python Version\n\n.. image:: https://img.shields.io/pypi/v/s3-parse-url\n  :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/l/s3-parse-url\n :alt: PyPI - License\n\n\n.. image:: https://coveralls.io/repos/github/marazmiki/s3-parse-url/badge.svg?branch=master\n :target: https://coveralls.io/github/marazmiki/s3-parse-url?branch=master\n\n.. image:: https://img.shields.io/codacy/grade/80c1a1af099848ddb5cc86221723f8d5\n  :alt: Codacy grade\n\n-----\n\nParses S3 credentials from the given string and returns it in comfortable\nformat to pass to popular clients like boto3.\n\nAbout\n=====\n\nThis is a small utility to parse locations of buckets of S3-compatible\nstorage (and, of course, the original Amazon\'s S3 itself) given in the URL form\nlike ``s3://bucket/``.\n\nIt could be useful in our epoch of the 12-factor applications when it\'s a\ngood practice to store credentials inside of environment variables.\n\nAlso, these days, there are some notable S3-compatible storage services:\n\n* `Selectel <https://>`_\n\n* `MinIO <https://min.io>`_ `(a self-hosted solution extremely handy for testing)`\n\nAnd dozens of others.\n\nWith ``s3-parse-url``, you can use any one of these services with no doubts about\nconfiguration endpoints. For example, you can connect to your Selectel storage\nwith ``boto3`` just using ``selectel://my-bucket`` DSN.\n\nThat\'s an example, what it was all about:\n\n.. code:: python\n\n    from s3_parse_url import s3_parse_url\n    from s3_parse_url.ext.clients import get_boto3_client\n\n    dsn = "s3://AKIA***OO:XP***@my-bucket/?region=us-east-2"\n\n    # It\'s a completely ready boto3 client instance to work with Selectel\n    s3_client = get_boto3_client(dsn)\n\nOf course, in the code above we worked with Selectel (have you ever heard\nabout it?). You can work this way with any S3 compatible storage. If you\nprefer unknown storage, you can easily create a plugin to add support for\nyour favorite service. Or, if you are a pervert, you can use a universal ``S3://``\nscheme, but in this case, you should manage endpoints by yourself:\n\n.. code:: python\n\n    from s3_parse_url.ext.clients import get_boto3_client\n\n    # Also should work\n    dsn = "s3://my-minio-user:my-minio-pass@minio.example.com:9000/?region=us-east-1"\n\n    # A ready client to work with a minio instance\n    s3_client = get_boto3_client(dsn)\n\n\nSupported providers\n===================\n\nCurrently we have support for these storages\n\n* Amazon S3\n* Selectel\n* Yandex\n* Mail.ru\n* MinIO\n\nBut you can easily add your own one.\n\nLicense\n=======\n\nThis project is licensed under the terms of the MIT license.\n\n',
    'author': 'Mikhail Porokhovnichenko',
    'author_email': 'marazmiki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marazmiki/s3-parse-url',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
