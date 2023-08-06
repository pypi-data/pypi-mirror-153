import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='site-configuration-client',
    version='0.1.8',
    description='Python client library for Site Configuration API',
    long_description=read('README.rst'),
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0",
    ],
    entry_points={
        'lms.djangoapp': [
            'site_config_client = site_config_client.apps:SiteConfigApp',
        ],
    },
    url="https://github.com/appsembler/site-configuration-client"
)
