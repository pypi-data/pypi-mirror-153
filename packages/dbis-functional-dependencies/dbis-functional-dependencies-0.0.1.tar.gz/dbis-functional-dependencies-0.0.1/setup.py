import pathlib
from setuptools import setup

class Version(object):
    name="relational_model"
    description="RWTH Aachen Computer Science i5/dbis assets for Lecture Datenbanken und Informationssysteme"
    version='0.0.1'

# The directory containing this file
HERE = pathlib.Path(__file__).parent.resolve()

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dbis-functional-dependencies",
    version=Version.version,
    description=Version.description,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/rwth-acis/dbis-relational-model.git",
    author="Wolfgang Fahl",
    author_email="fahl@dbis.rwth-aachen.de",
    license="Apache",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    packages=["functional_dependencies"],
    include_package_data=True,
    install_requires=[]
)
