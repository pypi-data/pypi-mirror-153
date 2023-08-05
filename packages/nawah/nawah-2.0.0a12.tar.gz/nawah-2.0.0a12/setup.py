'''Python package setup for Nawah Framework'''

from distutils.command.install import install

import setuptools

from nawah import __version__


class Version(install):
    '''Provides setup command to print Nawah Framework version'''

    def run(self):
        print(__version__)


class ApiLevel(install):
    '''Provides setup command to print Nawah Framework API Level'''

    def run(self):
        print('.'.join(__version__.split('.')[:2]))


with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()

with open('./requirements.txt', 'r', encoding='UTF-8') as f:
    requirements = f.readlines()

with open('./dev_requirements.txt', 'r', encoding='UTF-8') as f:
    dev_requirements = f.readlines()

setuptools.setup(
    name='nawah',
    version=__version__,
    author='Mahmoud Abduljawad',
    author_email='mahmoud@masaar.com',
    description='Nawah framework--Rapid app development framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nawah-io/nawah_framework',
    package_data={
        'nawah': ['version.txt', 'py.typed'],
        'nawah.cli': ['py.typed'],
        'nawah.base': ['py.typed'],
        'nawah.classes': ['py.typed'],
        'nawah.exceptions': ['py.typed'],
        'nawah.types': ['py.typed'],
        'nawah.config': ['py.typed'],
        'nawah.data': ['py.typed'],
        'nawah.enums': ['py.typed'],
        'nawah.utils': ['py.typed'],
        'nawah.utils._app': ['py.typed'],
        'nawah.utils._validate': ['py.typed'],
        'nawah.testing': ['py.typed'],
        'nawah.packages': ['py.typed'],
        'nawah.packages.core': ['py.typed'],
        'nawah.packages.core.base': ['py.typed'],
        'nawah.packages.core.file': ['py.typed'],
        'nawah.packages.core.group': ['py.typed'],
        'nawah.packages.core.session': ['py.typed'],
        'nawah.packages.core.setting': ['py.typed'],
        'nawah.packages.core.user': ['py.typed'],
    },
    packages=[
        'nawah',
        'nawah.cli',
        'nawah.base',
        'nawah.classes',
        'nawah.exceptions',
        'nawah.types',
        'nawah.config',
        'nawah.data',
        'nawah.enums',
        'nawah.utils',
        'nawah.utils._app',
        'nawah.utils._validate',
        'nawah.testing',
        'nawah.packages',
        'nawah.packages.core',
        'nawah.packages.core',
        'nawah.packages.core.base',
        'nawah.packages.core.file',
        'nawah.packages.core.group',
        'nawah.packages.core.session',
        'nawah.packages.core.setting',
        'nawah.packages.core.user',
    ],
    project_urls={
        'Docs: Github': 'https://github.com/nawah-io/nawah_docs',
        'GitHub: issues': 'https://github.com/nawah-io/nawah_framework/issues',
        'GitHub: repo': 'https://github.com/nawah-io/nawah_framework',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: AsyncIO',
    ],
    python_requires='>=3.10.2',
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    cmdclass={
        'version': Version,
        'api_level': ApiLevel,
    },
    entry_points={
        'console_scripts': {
            'nawah = nawah.__main__:main',
        }
    },
    zip_safe=False,
)
