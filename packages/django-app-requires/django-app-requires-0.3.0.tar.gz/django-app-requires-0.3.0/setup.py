# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]


setup(
    name="django-app-requires",
    version="0.3.0",
    description="A simple tool that allows you to specify app dependencies and middleware dependencies in your application, and also allow you to add default values for your additional configurations, after then load all your application settings into your project's settings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["django utils"],
    install_requires=requires,
    packages=find_packages(".", exclude=["django_app_requires_demo", "django_app_requires_example", "django_app_requires_example.migrations"]),
    zip_safe=False,
    include_package_data=True,
)