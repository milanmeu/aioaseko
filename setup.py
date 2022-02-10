from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aioaseko",
    version="0.0.2",
    author="Milan Meulemans",
    author_email="milan.meulemans@live.be",
    description="Async Python package for the Aseko Pool Live API",
    keywords="aseko pool live api asin aqua",
    license="LGPLv3+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/milanmeu/aioaseko",
    project_urls={
        "Say Thanks!": "https://saythanks.io/to/milan.meulemans@live.be",
        "Bug Tracker": "https://github.com/milanmeu/aioaseko/issues",
        "Source Code": "https://github.com/milanmeu/aioaseko",
        "Documentation": "https://github.com/milanmeu/aioaseko/blob/main/README.md",
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
    python_requires=">=3.8",
    packages=["aioaseko"],
    package_data={"aioaseko": ["py.typed"]},
    install_requires=["aiohttp"]
)
