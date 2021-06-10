# -*- coding: utf-8 -*-
import io

from setuptools import find_packages, setup


with io.open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='raven',
    description=('Backend Application for Ultrasound'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1-dev',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': ['raven=raven.cli:cli']},
    install_requires=[
        'click>=7.1.2',
        'Flask-AppBuilder>=3.2.0',
        'Flask-Migrate>=2.7.0',
        'psycopg2-binary>=2.8.6',
        'gunicorn>=20.0.4',
        'slixmpp>=1.7.0',
        'requests>=2.25.1',
    ],
    python_requires='~=3.8',
    author='David Ding',
    author_email='chengjie.ding@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)
