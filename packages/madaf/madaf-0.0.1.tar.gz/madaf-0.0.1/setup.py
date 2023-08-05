from setuptools import setup, find_packages

with open("requirements.txt") as fd:
    install_requires = fd.read().splitlines()

setup(
    name="madaf",
    version="0.0.1",
    description="Super fast key-value database similar to shelve",
    long_description=open("README.rst").read(),
    keywords="database",
    author="JJ Ben-Joseph",
    author_email="etz@memoriesofzion.com",
    python_requires=">=3.6",
    url="https://www.github.com/etz4ai/madaf",
    license="Apache",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=["pytest"],
)