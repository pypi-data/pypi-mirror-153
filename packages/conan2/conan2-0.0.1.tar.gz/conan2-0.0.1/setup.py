import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conan2",
    version="0.0.1",
    author="aoi togashi",
    author_email="atogashi@sciencepark.co.jp",
    description="A package for visualizing international tourism of up to 4 countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TogashiAoi/TRIP",
    project_urls={
        "Bug Tracker": "https://github.com/TogashiAoi/TRIP",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['conan2'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'conan2 = conan2:main'
        ]
    },
)


