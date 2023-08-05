# Always prefer setuptools over distutils
from setuptools import setup

# To use a consistent encoding
from codecs import open

setup(
    name="minos-judge",
    version="0.1.1",
    description="Demo library",
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    url="https://minos.readthedocs.io/",
    author="AnatoliyChudakov",
    author_email="anatoliy.chudakov020@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["judge"],
    include_package_data=True,
    install_requires=["numpy", "mlxtend", "scipy", "numpy", "pandas", "statsmodels"]
)