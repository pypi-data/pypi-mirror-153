import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.8.2' 
PACKAGE_NAME = 'aws_utils_lib' 
AUTHOR = 'Jonathan E. Aguiar' 
AUTHOR_EMAIL = 'jonathtanm@gmail.com' 
URL = 'https://github.com/swanm96'

LICENSE = 'MIT'
DESCRIPTION = 'AWS utils library ' 
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'boto3',
      ]
 
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)