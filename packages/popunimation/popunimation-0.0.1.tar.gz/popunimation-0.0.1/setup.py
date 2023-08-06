import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="popunimation",
    version="0.0.1",
    author="masaki yamamoto",
    author_email="yamamoto.ma25@gmail.com",
    description="A package for visualizing population of countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myamamoto325/population",
    project_urls={
        "Bug Tracker": "https://github.com/myamamoto325/population",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['popunimation'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'popunimation = popunimation:main'
        ]
    },
)
