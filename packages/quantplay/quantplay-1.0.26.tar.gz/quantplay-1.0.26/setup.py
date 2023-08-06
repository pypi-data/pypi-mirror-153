import re
from path import Path
from setuptools import setup, find_packages


def is_requirement(s: str) -> bool:
    """Returns true if the string is a valid requirement.
    For the requirement to be valid, it must be non empty
    and must not start from - or #.
    """
    s = s.strip()
    return not any([not s, re.match("^[-#]", s)])  # empty  # option or comment


requirements = [
    line.strip()
    for line in Path("requirements.txt").read_text().splitlines()
    if is_requirement(line)
]

setup(
    name="quantplay",
    long_description=Path("README.md").read_text(),
    version="1.0.26",
    setup_requires=["pytest-runner"],
    install_requires=requirements,
    tests_require=[],
    packages=find_packages(),
    url="",
    license="MIT",
    author="",
    author_email="",
    description="This python package will be stored in AWS CodeArtifact",
)
