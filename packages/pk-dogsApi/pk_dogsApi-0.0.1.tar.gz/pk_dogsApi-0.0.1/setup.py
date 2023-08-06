from pathlib import Path
from importlib_metadata import entry_points
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.1'
DESCRIPTION = 'Extrae un listado de razas de perros de la Api Pública de Dogs'
PACKAGE_NAME = 'pk_dogsApi'
AUTHOR = 'AntoGzz'
EMAIL = 'quirozd70@gmail.com'
GITHUB_URL = 'https://github.com/AntoGzz/'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    entry_points={
        'console_scripts': [
            # Cuando alguien instale el paquete y ejecute el comando py_pk_cf, se ejecutara el resto de la linea , es decir, el comando
            'pydogs=ppk_dogsApi.__main__:main',
        ],
    },
    version = VERSION,
    license='MIT',
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author = AUTHOR,
    author_email = EMAIL,
    url = GITHUB_URL,
    keywords = [],
    install_requires=[ 
        'requests',
        'twine'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)