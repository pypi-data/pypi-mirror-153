import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="earthquake-in-indonesia",
    version="0.0.4",
    author="Hendra Kusuma",
    author_email="hendrakusuma.vegas@gmail.com",
    description="This package will help you to retrieve data from the [BMKG]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Henzo-Kawaii/latest-information-earthquake-update--indonesia",
    project_urls={
        "Website": "https://henzogagerz.blogspot.com/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)


