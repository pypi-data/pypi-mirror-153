from io import open
from setuptools import setup

"""
:authors: FranChesKo
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2022 FranChesKo
"""

version = '1.1.1.2'

long_description = """Python module for creating graphs using files"""

setup(
    name='graphcreator',
    version=version,

    author='FranChesKo',
    author_email='khl_doss@mail.ru',

    description='Python module for creating graphs using files',
    long_description=long_description,

    url='https://github.com/FranChesK0/GraphCreator',
    download_url=f'https://github.com/FranChesK0/GraphCreator/archive/v{version}',

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['graphcreator'],
    install_requires=['numpy', 'matplotlib'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
