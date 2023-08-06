from importlib.metadata import entry_points
from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.2'
DESCRIPTION = 'This package allows you to consume the EndPoint of CodigoFacilito workshops.'
PACKAGE_NAME = 'pycodigof'
AUTHOR = 'Hazael Jiménez'
EMAIL = 'jejibarrera@gmail.com'
GITHUB_URL = 'https://github.com/HazaelJDev/python_package'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    entry_points = {
        "console_scripts": [
            "pycody=pycodigof.__main__:main"
        ]
    },
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = ['codigofacilito'],
    install_requires=[ 
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)