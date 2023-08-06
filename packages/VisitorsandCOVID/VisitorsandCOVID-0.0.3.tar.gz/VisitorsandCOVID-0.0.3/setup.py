import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VisitorsandCOVID",
    version="0.0.3",
    author="rinko takei",
    author_email="rtakei@sciencepark.co.jp",
    description="This project compares the number of amusement park visitors with COVID infected people.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ritakei/VisitorsandCOVID",
    project_urls={
        "Bug Tracker": "https://github.com/ritakei/VisitorsandCOVID",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['VisitorsandCOVID'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10.4",
    entry_points = {
        'console_scripts': [
            'VisitorsandCOVID = VisitorsandCOVID:main'
        ]
    },
)
