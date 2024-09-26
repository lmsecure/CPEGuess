from setuptools import setup, find_packages
import os
import re

with open("cpeguess/requirements.txt", "r") as file:
    requirements = [package.strip() for package in file]

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('cpeguess/')


setup(
    name="cpeguess",
    version="0.0.1b",
    url="https://github.com/lmsecure/CPEGuess",
    author="LMSecurity",
    author_email="lm.security@lianmedia.ru",
    description="Package for finding cpe",
    license="MIT",
    keywords=['penetration testing', 'cpe'],
    packages=["cpeguess"],
    package_data={"": extra_files},
    install_requires=requirements,
    entry_points={
        "console_scripts": ["cpeguess = cpeguess.__init__:run"],
    },
    python_requires='>=3.12',
)
