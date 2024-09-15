from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aioaseko",
    version="1.0.0",
    author="Milan Meulemans",
    author_email="milan.meulemans@live.be",
    description="Async Python package for the Aseko Pool Live API",
    keywords="aseko pool live api asin aqua",
    license="LGPLv3+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/milanmeu/aioaseko",
    project_urls={
        "Homepage": "https://github.com/milanmeu/aioaseko",
        "Bug Tracker": "https://github.com/milanmeu/aioaseko/issues",
        "Source Code": "https://github.com/milanmeu/aioaseko/tree/main/aioaseko",
        "Documentation": "https://github.com/milanmeu/aioaseko/blob/main/README.md",
        "Donate": "https://github.com/sponsors/milanmeu",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Home Automation",
        "Typing :: Typed",
    ],
    python_requires=">=3.10",
    packages=["aioaseko"],
    package_data={"aioaseko": ["py.typed"]},
    install_requires=["aiohttp", "gql", "apischema"]
)
