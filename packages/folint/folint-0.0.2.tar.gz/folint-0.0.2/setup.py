import pathlib
from importlib_metadata import entry_points
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="folint",
    version="0.0.2",
    description="Linter for FOdot used in the IDP-Z3 system",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/larsver/folint",
    author="larsver",
    author_email="lars.larsvermeulen@gmail.com",
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development'
      ],
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['ast_engine/Idp.tx']},
    install_requires=["textX","z3-solver"],
    entry_points = {
      'console_scripts': ['folint=folint.SCA:main']
    }
)
