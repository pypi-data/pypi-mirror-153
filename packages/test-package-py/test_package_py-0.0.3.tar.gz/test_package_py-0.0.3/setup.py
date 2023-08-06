from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.3'
DESCRIPTION = 'Permite consumir el API de CodigoFacilito.'
PACKAGE_NAME = 'test_package_py'
AUTHOR = 'Lucas Ollarce'
EMAIL = 'luk5ollarce@gmail.com'
GITHUB_URL = 'https://github.com/Ollyxs/python_package_test'

setup(
    name = PACKAGE_NAME,
    packages = [PACKAGE_NAME],
    entry_points = {
        "console_scripts": 
            ["pytestcody=test_package_py.__main__:main"]
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
        'codigofacilito', 'ollyxs'
        ],
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
