from json import load

import setuptools


def locked_requirements(section = 'default'):
    """Look through the 'Pipfile.lock' to fetch requirements by section."""
    with open('Pipfile.lock') as pip_file:
        pipfile_json = load(pip_file)

    if section not in pipfile_json:
        print(f'Error: Section "{section}" is missing from "Pipfile.lock" file.')
        return []

    return [package + detail.get('version', '') for package, detail in pipfile_json[section].items()]


with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'datetime_toolkit',
    version = '1.0.1',
    author = 'Sebastián Valdivia Loyola',
    author_email = 'admin@svaldivia.cl',
    description = 'Python package to work with NTP servers, time zones, and localized names of months and days of the week.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/svaldivia12/datetime_toolkit',
    packages = setuptools.find_packages(),
    keywords = 'Datetime Toolkit',
    classifiers = ['Programming Language :: Python :: 3',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent'],
    install_requires = locked_requirements(),
)
