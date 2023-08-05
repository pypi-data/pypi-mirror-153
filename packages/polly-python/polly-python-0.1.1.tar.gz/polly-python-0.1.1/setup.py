import pathlib
import os
from setuptools import setup, find_packages

UPSTREAM_URLLIB3_FLAG = "--with-upstream-urllib3"


def get_requirements(raw=False):
    """Build the requirements list for this project"""
    requirements_list = []

    with open("requirements.txt") as reqs:
        for install in reqs:
            if install.startswith("# only telegram.ext:"):
                if raw:
                    break
                continue
            requirements_list.append(install.strip())

    return requirements_list


def get_packages_requirements(raw=False):
    """Build the package & requirements list for this project"""
    reqs = get_requirements(raw=raw)
    exclude = ["tests*"]
    packs = find_packages(exclude=exclude)
    return packs, reqs


packages, requirements = get_packages_requirements()
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# This call to setup() does all the work
# circle bracket and format in the download_url parameter to resolve linting issue
# of line too long
setup(
    name="polly-python",
    version=get_version("polly/__init__.py"),
    description="Polly SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=packages,
    include_package_data=True,
    setup_requires=["wheel"],
    install_requires=requirements,
    url="https://github.com/ElucidataInc/polly-python",
    download_url=(
        "https://elucidatainc.github.io/PublicAssets/builds/polly-python/"
        "polly_python-{a}-none-any.whl".format(a=get_version("polly/__init__.py"))
    ),
)
