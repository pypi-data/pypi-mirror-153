# This file is part of flask_tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import io
import os
import re
from setuptools import setup


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_version():
    init = read('flask_tryton.py')
    return re.search("__version__ = '([0-9.]*)'", init).group(1)


setup(name='flask_tryton',
    version=get_version(),
    author='B2CK',
    author_email='info@b2ck.com',
    url='http://flask-tryton.b2ck.com/',
    description='Adds Tryton support to Flask application',
    long_description=read('README'),
    py_modules=['flask_tryton'],
    zip_safe=False,
    platforms='any',
    keywords='flask tryton web',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Tryton',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
    license='GPL-3',
    python_requires='>=3.5',
    install_requires=[
        'Flask>=0.8',
        'Werkzeug',
        'trytond>=5.0',
        ],
    )
