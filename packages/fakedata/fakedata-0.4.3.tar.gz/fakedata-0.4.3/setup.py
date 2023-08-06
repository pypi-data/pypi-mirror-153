from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.4.3'
DESCRIPTION = 'A python package for data fake generation'
PACKAGE_NAME = 'fakedata'
AUTHOR = 'Jose Angel Colin Najera'
EMAIL = 'josecolin99@gmail.com'
GITHUB_URL = 'https://github.com/Josecolin99/FakeData'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    entry_points={
        "console_scripts":
            ["fakedata=fakedata.__main__:main"]
    },
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = [
        'FakeData',
        'Fake Data',
        'fakedata',
        'faked ata',
        'Data',
        'data'
    ],
    install_requires=[ 
        
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)