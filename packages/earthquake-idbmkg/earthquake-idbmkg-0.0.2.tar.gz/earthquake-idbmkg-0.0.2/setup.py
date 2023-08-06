import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="earthquake-idbmkg",
    version="0.0.2",
    author="Todi Rahmat",
    author_email="todirahmat123@gmail.com",
    description="This package will get the latest eartquake data from BMKG | Indonesia Meteorological, Climatological, "
                "and Geophysical Agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coach-of-kopycode/realtime-indonesia-earthquake",
    project_urls={
        "Website": "https://todikun.github.io/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
