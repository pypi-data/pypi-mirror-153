import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jpaccident",
    version="0.0.2",
    author="Tsuyoshi Hine",
    author_email="tsuyoshi.h0920@gmail.com",
    description='Package for visualization of aggregate data on fatalities in traffic accidents',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/s2022027/jpaccident",
    project_urls={
        "Bug Tracker": "https://github.com/s2022027/jpaccident",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['jpaccident'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'jpaccident = jpaccident:main'
        ]
    },
)
