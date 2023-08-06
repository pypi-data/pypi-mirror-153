import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cioat",
    version="0.0.1",
    author="JIAOYANG XU",
    author_email="jiaoyangxu307@gmail.com",
    description="COVID-19's Impact on Airport Traffic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jiaoyang-x/covidT",
    project_urls={
        "Bug Tracker": "https://github.com/jiaoyang-x/covidT",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['cioat'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'cioat = cioat:main'
        ]
    },
)
