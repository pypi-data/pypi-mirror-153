import setuptools

with open("VERSION", "r") as infile:
    version = infile.read().strip()

with open("README.md", "r", encoding="utf-8") as infile:
    readme = infile.read()

packagedir = "src"

setuptools.setup(
    name="dgbowl-schemas",
    version=version,
    author="Peter Kraus",
    author_email="peter@tondon.de",
    description="schemas for the dgbowl suite of tools",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/dgbowl/dgbowl-schemas",
    project_urls={
        "Bug Tracker": "https://github.com/dgbowl/dgbowl-schemas/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": packagedir},
    packages=setuptools.find_packages(where=packagedir),
    python_requires=">=3.9",
    install_requires=[
        "pydantic>=1.8",
        "pyyaml>=5.0"
    ],
    extras_require={
        "testing": [
            "pytest"
        ],
        "docs": [
            "sphinx==4.5.0",
            "sphinx-rtd-theme",
            "sphinx-autodoc-typehints",
            "autodoc-pydantic"
        ]
    }
)
