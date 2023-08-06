from distutils.core import setup
from setuptools import find_namespace_packages

VERSION = '0.2a2'

setup(
    name="tokyo-annotation",
    packages=find_namespace_packages('tokyo_annotation', include=['tokyo_annotation.*']),
    version=VERSION,
    license="MIT",
    description="Tokyo Annotation",
    author="Dion Ricky Saputra",
    author_email="code@dionricky.com",
    url="https://github.com/dion-ricky/tokyo-annotation",
    keywords=["data annotation"],
    install_requires=[
        "attrs==19.3.0",
        "certifi==2020.6.20",
        "charset-normalizer==2.0.12",
        "idna==2.10",
        "openlineage-python==0.5.1",
        "requests==2.24.0",
        "urllib3==1.25.10"
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
