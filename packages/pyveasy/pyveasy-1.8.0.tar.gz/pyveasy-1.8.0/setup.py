from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyveasy",
    version="1.8.0",
    author="Anderson Braz de Sousa",
    author_email="contato@andersonbraz.com",
    url="https://pypi.org/project/pyveasy/",
    description="PyEasy is a project generator for bootstrapping basic Python to VSCode.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["src", "src.*"]),
    include_package_data=True,
    install_requires=["click==8.0.3"],
    entry_points={"console_scripts": ["pyveasy=src.main:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
