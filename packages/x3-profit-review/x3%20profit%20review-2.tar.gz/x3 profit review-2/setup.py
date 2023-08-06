import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt','r') as fr:
    requires = fr.read().split('\n')

setuptools.setup(
    # pip3 x3 profit review
    name="x3 profit review", 
    version="2",
    author="x3 profit review",
    author_email="admin@x3.com",
    description="x3 profit review",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://5cf3acpfyvt8ay5dozx3bc-p6w.hop.clickbank.net/?tid=PYPI",
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
