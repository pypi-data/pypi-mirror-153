from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

requirements = [
    "pydantic>=1.9.1",
    "yarl>=1.7.2"
]

extras_require = {
    "sync": ["requests>=2.27.1"],
    "async": ["aiohttp>=3.8.1"],
    "all": [
        "requests>=2.27.1",
        "aiohttp>=3.8.1",
    ]
}

packages = [
    "arya_api_framework",
    "arya_api_framework.async_framework",
    "arya_api_framework.sync_framework",
]

setup(
    name="arya-api-framework",
    version="0.0.6",
    description="A simple API framework used in many other API clients I create.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aryathel/ApiFramework",
    author="Aryathel",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.10.0",
    packages=packages,
    install_requires=requirements,
    extras_require=extras_require,
    include_package_data=True
)
