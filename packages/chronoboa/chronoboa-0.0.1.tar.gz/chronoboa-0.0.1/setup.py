from pathlib import Path # > 3.6
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.1'
DESCRIPTION = 'Paquete permite consumir el API de CodigoFacilito'
PACKAGE_NAME = 'chronoboa'
AUTHOR = 'Victoriano'
EMAIL = 'mytacam78@gmail.com'
GITLAB_URL = 'https://gitlab.com/V-Juarez/cruds/-/tree/pypi'

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=GITLAB_URL,
    keywords=[
      'codigofacilto'
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
