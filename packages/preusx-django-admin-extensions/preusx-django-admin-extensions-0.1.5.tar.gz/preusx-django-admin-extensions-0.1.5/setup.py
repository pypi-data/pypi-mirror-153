import os
import re
import setuptools


with open('README.md', 'r') as rf:
    with open('CHANGELOG.md', 'r') as cf:
        long_description = rf.read() + cf.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()

    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)


version = get_version('pxd_admin_extensions')


setuptools.setup(
    name='preusx-django-admin-extensions',
    version=version,
    author='Alex Tkachenko',
    author_email='preusx@gmail.com',
    license='MIT License',
    description='Utilities and extensions for django administration panel.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=(),
    extras_require={
        'contrib': (
            'django-admin-rangefilter==0.6.3',
            'django-admin-numeric-filter==0.1.6',
            'django-admin-easy==0.6',
            'django-better-admin-arrayfield==1.4.2',
        ),
        'docs': (
            'mkdocs==1.1.2',
            'mkdocstrings==0.14.0',
            'mkdocs-material==6.2.4',
            'mkdocs-include-markdown-plugin==3.3.0',
        ),
        'dev': (
            'pytest>=6.0,<7.0',
            'pytest-watch>=4.2,<5.0',
            'pytest-django>=4.3,<5.0',
            'django-environ==0.4.5',
            'django-stubs',
            'django>=2.2,<4',
            'twine',
        ),
    },
    include_package_data=True,
    packages=setuptools.find_packages(exclude=(
        'tests', 'tests.*',
        'example', 'example.*',
        'docs', 'docs.*',
    )),
    python_requires='>=3.6',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',

        'Programming Language :: Python :: 3',

        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
