import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pyut2xml",
    version="0.1.1",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Pyut decompressor',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/pyut2xml",
    packages=[
        'pyut2xml'
    ],
    install_requires=['click'],
    entry_points='''
        [console_scripts]
        pyut2xml=pyut2xml.pyut2xml:commandHandler
    ''',
)
