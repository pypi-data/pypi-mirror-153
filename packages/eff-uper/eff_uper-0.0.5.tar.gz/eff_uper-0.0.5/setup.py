import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eff_uper",
    version="0.0.5",
    author="Miu Takahashi",
    author_email="s2022046@stu.musashino-u.ac.jp",
    description='Numerical values used to evaluate the contribution of basketball players in the B1 League (2016-2021) Python Package to compare "EFF" and "uPER" by year',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/haku-19/eff_uper.git",
    project_urls={
        "Bug Tracker": "https://github.com/haku-19/eff_uper.git",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    package_dir={"": "src"},
    py_modules=['eff_uper'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'eff_uper = eff_uper:main',
        ]
    },
)