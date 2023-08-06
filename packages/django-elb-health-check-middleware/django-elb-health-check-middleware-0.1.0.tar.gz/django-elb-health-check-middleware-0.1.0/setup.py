from os.path import exists

from setuptools import find_packages, setup

setup(
    name="django-elb-health-check-middleware",
    author="Bill Schumacher",
    author_email="william.schumacher@gmail.com",
    packages=find_packages(),
    scripts=[],
    url="https://github.com/BillSchumacher/django-elb-health-check-middleware",
    license="MIT",
    description="Process ELB health checks efficiently, no crazy IP lookups.",
    long_description=open("README.rst").read() if exists("README.rst") else "",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=["django"],
    version="0.1.0",
    zip_safe=False,
)
