import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def scripts( ):
    return [os.path.join( 'bin', f ) for f in os.listdir( 'bin' )]

__version__ = "1.1.0"

setup(
    name = "pyAgileTaskEmailImport",
    version = __version__,
    author = "Tyghe Vallard",
    author_email = "vallardt@gmail.com",
    description = ("Imports emails that match a certain criteria into AgileTask.me"),
    keywords = "import email agiletask",
    url = "https://github.com/necrolyte2/Python-Agile-Task-Email-Importer",
    packages = [],
    scripts = scripts(),
    data_files = [
    ],
    install_requires = [
        "pyAgileTaskAPI >=1.1.0",
    ],
    long_description=read('README.md'),
)
