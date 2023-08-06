import os
from os import path
import shutil
import subprocess

from setuptools import find_packages
from setuptools import setup
from setuptools.command.sdist import sdist

VERSION = "7.2.5"

install_requires = [
    "flask==2.1.2",
    "pika==1.0.1",
    "pymongo==3.12.2",
    "flask-cors==3.0.10",
    "flask-jwt-extended==4.4.0",
    "dnspython==1.16.0",
    "jsonschema==3.0.1",
    "apscheduler==3.6.0",
    "sentry-sdk==1.5.1",
    "redis==3.5.3",
    "tzlocal<3.0",
    # contrib
    "oauthlib==3.1.0",
    "requests<3.0.0",
    "python-twitter==3.5",
]

tests_require = [
    "mongomock==3.23.0",
]

setup_requires = [
    "flake8",
    "black",
    "setuptools-black",
    "flake8-black",
    "flake8-import-order",
    "flake8-bugbear",
]


WEB_ARTIFACT_PATH = os.path.join("broccoli_server", "web")


def build_web():
    # check executables which are required to build web
    if not shutil.which("node"):
        raise RuntimeError("node is not found on PATH")
    if not shutil.which("yarn"):
        raise RuntimeError("yarn is not found on PATH")

    # build web
    subprocess.check_call(["yarn", "install"], cwd="web")
    subprocess.check_call(["yarn", "build"], cwd="web")

    # move built artifact
    if os.path.exists(WEB_ARTIFACT_PATH):
        print("removing old web artifact")
        shutil.rmtree(WEB_ARTIFACT_PATH)
    shutil.move(os.path.join("web", "build"), WEB_ARTIFACT_PATH)


class SdistCommand(sdist):
    def run(self):
        build_web()
        sdist.run(self)


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="broccoli_server",
    version=VERSION,
    description="A Python framework to build web scraping applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/k-t-corp/broccoli-server",
    author="KTachibanaM",
    author_email="whj19931115@gmail.com",
    license_files=("LICENSE",),
    packages=find_packages(),
    # this is important for including web when building wheel
    include_package_data=True,
    # this is important for including web when building wheel
    package_data={"broccoli_server": ["web"]},
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    setup_requires=setup_requires,
    test_suite="broccoli_server.tests",
    cmdclass={"sdist": SdistCommand},
)
