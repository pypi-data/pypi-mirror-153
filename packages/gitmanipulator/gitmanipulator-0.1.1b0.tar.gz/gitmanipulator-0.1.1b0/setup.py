from pip._internal.req import parse_requirements
from setuptools import setup, find_packages
from gitmanipulator.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='gitmanipulator',
    version=VERSION,
    description='manipulate many git project',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Alex',
    author_email='',
    url='',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'gitmanipulator': ['templates/*']},
    install_requires=[
        "cement==3.0.6",
        "jinja2",
        "pyyaml",
        "colorlog",
        "tinydb~=4.7.0",
        "GitPython",
        "tqdm",
    ],
    include_package_data=True,
    entry_points="""
        [console_scripts]
        gitmanipulator = gitmanipulator.main:main
    """,
)
