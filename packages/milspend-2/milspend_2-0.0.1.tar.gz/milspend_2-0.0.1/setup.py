import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="milspend_2",
    version="0.0.1",
    author="nichiho yamauchi",
    author_email="s2022032@stu.musashino-u.ac.jp",
    description="Manufacturing Hourly Earnings 2017",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NichihoYamauchi/milspend_2.py",
    project_urls={
        "Bug Tracker": "https://github.com/NichihoYamauchi/milspend_2.py",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['milspend_2'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'milspend_2 = milspend_2:main'
        ]
    },
)
