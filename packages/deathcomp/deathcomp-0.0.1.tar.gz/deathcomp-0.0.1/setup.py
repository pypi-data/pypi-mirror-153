import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deathcomp",
    version="0.0.1",
    author="runa yoshida",
    author_email="s2022067@stu.musashino-u.ac.jp",
    description="A package compares the number of deaths due to COVID-19 in two countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RunaYoshida/deathcomp",
    project_urls={
        "Bug Tracker": "https://github.com/RunaYoshida/deathcomp",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['deathcomp'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'deathcomp = deathcomp:main'
        ]
    },
)
