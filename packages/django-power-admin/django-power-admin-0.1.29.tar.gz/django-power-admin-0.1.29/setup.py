# -*- coding: utf-8 -*-
import os
import sys
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, 'requirements.txt'), "r", encoding="utf-8") as fobj:
    requires = [x.strip() for x in fobj.readlines() if x.strip()]

setup(
    name="django-power-admin",
    version="0.1.29",
    description="Django提供了快捷的生成后台管理站点的能力。本应用旨在增强Django Admin的能力，提供丰富的Admin、Widget、ListFilter、Form等等界面扩展类，同时也为常用的数据管理模型提供完整的管理功能。",
    long_description=long_description,
    long_description_content_type='text/markdown',
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
    keywords=["django", "django admin", "django power admin", "django admin extensions"],
    install_requires=requires,
    packages=find_packages(".", exclude=["django_power_admin_demo", "django_ucenter", "django_ucenter.migrations", "django_power_admin_example", "django_power_admin_example.migrations"]),
    include_package_data=True,
    zip_safe=False,
)