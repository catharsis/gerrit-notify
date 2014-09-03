#coding=utf-8
from setuptools import setup, find_packages
from subprocess import check_output

def get_version():
	tag = check_output(["git", "tag"])
	hash = check_output(["git", "log", "-1", "--format=%H"])[:10]
	return "%s-p%s" % (tag, hash)

setup(
        name = "gerrit-notify",
        version = get_version(),
        packages = find_packages(),
        author = "Anton Löfgren",
        author_email = "anton.lofgren@gmail.com",
        license = "BSD (2-clause)",
        keywords = "gerrit review notify notification daemon",
        install_requires = open('requirements.txt').read().split('\n'),
        entry_points = {
            'console_scripts': [
                'gerrit-notify = gerrit_notify.main:main',
                ],
            }
        )
