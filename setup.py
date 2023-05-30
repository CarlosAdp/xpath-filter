from pathlib import Path
from setuptools import setup

from src import __prog__, __version__, __author__, __email__, __url__, \
    __description__, __keywords__, __license__


setup(
    name=__prog__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=open(Path(__file__).parent / "README.md").read(),
    license=__license__,
    url=__url__,
    keywords=__keywords__,
    classifiers=[
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Web scraping',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    packages=['xpath_filter'],
    package_dir={'xpath_filter': 'src'},
    install_requires=[
        'lxml',
        'PyYAML'
    ],
    extras_require={
        'test': [
            'pytest',
        ],
        'dev': [
            'flake8',
            'mypy'
        ]
    }
)
