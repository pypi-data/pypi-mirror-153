import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="farmquest",
    version="0.0.5",
    author="Régis Tremblay Lefrançois",
    author_email="rtlefrancois@agri-marche.com",
    description="Python package to interact with the FarmQuest WebService",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agri-marche/farmquest",
    project_urls={
        "Bug Tracker": "https://github.com/agri-marche/farmquest/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['requests']
)
