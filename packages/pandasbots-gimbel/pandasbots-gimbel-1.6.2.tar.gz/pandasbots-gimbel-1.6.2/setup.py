import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandasbots-gimbel",
    version="1.6.2",
    author="Rafael Klanfer Nunes",
    author_email="comercial@pandasbots.com",
    description="This package allows you to scrap Gimbel Mexicana website and return product infos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pandasbots.com",
    project_urls={
        "Source Code": "https://github.com/PandasBots/pandasbots-gimbel",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["pandas", "selenium", "webdriver-manager", "beautifulsoup4", "openpyxl"],
    python_requires=">=3.6",
    
)
