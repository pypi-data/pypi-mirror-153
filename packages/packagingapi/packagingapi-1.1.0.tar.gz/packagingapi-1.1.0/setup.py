from setuptools import setup, find_packages

install_requires = [
    'requests',
    'polling2',
    'urllib3',
    'mock',
    ]

setup(name='packagingapi',
version='1.1.0',
description='Test Package',
author='jiminlee',
author_email='jimin.lee@nota.ai',
install_requires=install_requires,
python_requires='>=3',
packages=find_packages(),
long_description_content_type="text/markdown",
long_description="Description",
)