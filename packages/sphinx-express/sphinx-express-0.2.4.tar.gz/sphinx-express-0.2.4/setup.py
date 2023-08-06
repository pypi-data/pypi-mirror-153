import io
import os

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent

def get_version(rel_path):
    for line in (this_directory / rel_path).read_text().splitlines():
        if line.startswith('__VERSION__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


LONG_DESCRIPTION = (this_directory / "README.md").read_text()
SHORT_DESCRIPTION = "Quick setup utility for sphinx"

requirements = [
    'typer>=0.3.2',
    'PyYAML>=5.3.1',
    'sphinx>=1.7.0',
]

setup(
    name='sphinx-express',
    version=get_version('sphinx_express/versions.py'),
    url="https://github.com/iisaka51/sphinx-express.git",
    author="Goichi (Iisaka) Yukawa",
    author_email="iisaka51@gmail.com",
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=requirements,
    dependency_links=[],
    extras_require={},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Shells',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Setuptools Plugin',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Printing',
        'Topic :: Software Development',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Utilities',
    ],
    platforms='any',
    entry_points={
        'console_scripts': [
            'sphinx-express = sphinx_express:app',
        ],
    },
    python_requires=">=3.6",

)
