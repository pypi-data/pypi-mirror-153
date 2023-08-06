# coding: utf-8
import os, re
from setuptools import setup, find_namespace_packages

version = '1.0.0'
appname = "u3driver"
with open(os.path.join("u3driver", "__init__.py"), encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)
    # for github action
    tag = os.getenv('tag')
    build_number = os.getenv('build_number')
    print(f'build_number={build_number}')
    if tag and tag.startswith("refs/tags/v"):
        version = tag.replace("refs/tags/v", "")
    elif build_number:
        version = version.replace("x", build_number)
    else:
        # add version
        x_y_z = [int(x) for x in version.split('.')]
        x_y_z[-1] += 1
        version = '.'.join(str(x) for x in x_y_z)

setup(
    name=appname,
    version=version,
    python_requires='>=3.6',
    description='u3driver',
    url='https://github.com/king3soft/u3driver',
    author='king3soft',
    author_email='buutuud@gmail.com',
    license='GPLv3',
    include_package_data=True,
    packages=find_namespace_packages(include=['u3driver.*', "u3driver"]),
    install_requires=''''''.split('\n'),
    zip_safe=False)
