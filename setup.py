import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="localstack-utils",
    description='An easy way to inclute Localstack with unit tests',
    version="0.0.1",
    author='Waldemar Hummer',
    author_email='waldemar.hummer@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "",
    },        
    license='Apache License 2.0',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Testing",
    ],
    package_dir={"": "localstack_utils"},
    packages=setuptools.find_packages(where="localstack_utils"),
    python_requires=">=3.6",
)