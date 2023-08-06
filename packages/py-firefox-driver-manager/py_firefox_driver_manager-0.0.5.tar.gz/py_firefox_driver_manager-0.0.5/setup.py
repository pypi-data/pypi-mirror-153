from setuptools import setup
import setuptools
import os
import sys

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

print(install_requires)
setup(
    name='py_firefox_driver_manager',
    version='0.0.5',
    license='',
    author='Hamed',
    author_email='hamed.minaei@gmail.com',
    description='manage install firfox and Gecko Driver',
    long_description=read_file('Readme.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/HamedMinaeizaeim/py-Gecko-FireFox-Driver-Manager",
    project_urls={
        "Bug Tracker": "https://github.com/HamedMinaeizaeim/py-Gecko-FireFox-Driver-Manager/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    packages=['py_firefox_driver_manager'],
    package_dir={'': 'src'},
    python_requires=">=3.6",
)
