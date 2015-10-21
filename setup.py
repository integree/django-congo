from setuptools import setup, find_packages
from congo import VERSION

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = 'django-congo',
    version = VERSION.replace(' ', '-'),
    description = 'Some useful tool for faster and more efficient Django application development.',
    long_description = readme(),
    author = 'Integree Bussines Solutions',
    author_email = 'dev@integree.pl',
    url = 'https://github.com/integree/django-congo',
    download_url = 'https://pypi.python.org/packages/source/d/django-congo/django-congo-%s.zip' % VERSION,
    keywords = 'django-congo congo django utils integree',
    packages = find_packages(),
    include_package_data = True,
    license = 'MIT License',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires = [
        'django-appconf',
        'py-moneyed',
    ],
    zip_safe = False)
