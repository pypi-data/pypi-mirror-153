import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_ldap_mails import __version__


try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="pretix-ldap-mails",
    version=__version__,
    description="Verify user supplied mails against LDAP",
    long_description=long_description,
    url="https://github.com/kagonlineteam/pretix-ldap-mails",
    author="strifel",
    author_email="info@strifel.de",
    license="Apache",
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_ldap_mails=pretix_ldap_mails:PretixPluginMeta
""",
)
