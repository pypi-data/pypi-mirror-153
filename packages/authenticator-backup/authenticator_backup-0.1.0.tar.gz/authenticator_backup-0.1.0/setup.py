from importlib.machinery import SourceFileLoader
from pathlib import Path
from subprocess import check_call

from setuptools import find_packages, setup
from setuptools.command.develop import develop

pwd = Path(__file__).parent

# Get the long description from the README file
with pwd.joinpath("README.md").open(encoding="utf-8") as f:
    long_description = f.read()


class LintCommand(develop):
    """Run linting"""

    def run(self):
        try:
            check_call("black .".split())
            check_call("isort --profile black .".split())
            check_call("autoflake -ir .".split())
        except CalledProcessError as err:
            if "non-zero" in str(err):
                print("linting failed with warnings", file=sys.stderr)
                sys.exit(1)


# Allows us to import the file without executing imports in module __init__
meta = SourceFileLoader(
    "meta", str(pwd.joinpath("authenticator_backup/_meta.py"))
).load_module()

setup(
    name="authenticator_backup",
    version=meta.version,
    description="Tool to backup Google Authenticator to a GPG encrypted file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikeshultz/authenticator_backup",
    author=meta.author,
    author_email=meta.email,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="google authenticator backup",
    packages=find_packages(exclude=["build"]),
    install_requires=[
        "opencv-python~=4.5.5.64",
        "python-gnupg~=0.4.9",
        "pyzbar~=0.1.9",
        "qrcode[pil]~=7.3.1",
    ],
    extras_require={
        "dev": [
            "autoflake~=1.4",
            "black>=21.11b1",
            "isort>=5.10.1",
            "mypy>=0.910",
            "setuptools>=44.0.0",
            "twine>=3.1.1",
            "wheel>=0.33.6",
        ],
    },
    package_data={
        "": [
            "README.md",
            "LICENSE",
        ],
    },
    cmdclass={
        "lint": LintCommand,
    },
)
