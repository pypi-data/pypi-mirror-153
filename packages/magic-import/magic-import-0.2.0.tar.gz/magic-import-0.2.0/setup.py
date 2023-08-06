import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "dictop",
]

if os.sys.version.startswith("2.6"):
    requires += [
        "importlib",
    ]

setup(
    name="magic-import",
    version="0.2.0",
    description="Import python object from string and return the reference of the object. The object can be a class, instance, variable and anything else, and can be from class, instance, module, global/local environment.",
    long_description=long_description,
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    license_files=("LICENSE",),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['magic-import'],
    requires=requires,
    install_requires=requires,
    packages=find_packages(".", exclude=["tests"]),
    py_modules=["magic_import"],
)