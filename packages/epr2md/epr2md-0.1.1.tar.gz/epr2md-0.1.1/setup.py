import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="epr2md",
    version="0.1.1",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Converts EPR files to Markdown',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/epr2mdl",
    packages=[
        'epr2md'
    ],
    install_requires=['click'],
    entry_points='''
        [console_scripts]
        epr2md=epr2md.epr2md:commandHandler
    ''',
)
