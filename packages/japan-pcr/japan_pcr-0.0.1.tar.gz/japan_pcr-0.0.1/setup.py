import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    setuptools.setup(
    name="japan_pcr",
    version="0.0.1",
    author="hayato kambara",
    author_email="s1922009@musashino-u.ac.jp",
    description="Displays the number of pcr tests performed per day to date in Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kambara123/japan_pcr",
    project_urls={
    "Bug Tracker": "https://github.com/ytakefuji/safety_vaccine",
    },
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['vaers'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
    'console_scripts': [
    'japan_pcr = japan_pcr:main'
    ]
    },
    )
