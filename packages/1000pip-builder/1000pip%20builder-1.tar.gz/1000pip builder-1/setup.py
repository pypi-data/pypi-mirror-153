import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 1000pip builder
    name="1000pip builder", 
    version="1",
    author="1000pip builder",
    author_email="1000pip@builder.com",
    description="1000pip builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bf031bojwy-4fr5xcr6mowbkfg.hop.clickbank.net/?tid=p",
    project_urls={
        "Bug Tracker": "https://github.com/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=requires,
)
