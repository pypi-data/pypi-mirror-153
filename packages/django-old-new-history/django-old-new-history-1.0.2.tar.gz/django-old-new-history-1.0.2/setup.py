import os, sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    try:
        import wheel

        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='django-old-new-history',
    version='1.0.2',
    license='MIT',
    description="Show the old and new value of model's change field in history.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mayur Ariwala",
    author_email='mayur@softices.com',
    packages=['django_old_new_history'],
    include_package_data=True,
    url='https://github.com/Softices/django-old-new-history',
    keywords='Django Old New History',
    install_requires=[
        'django',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe=False,
)
