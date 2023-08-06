import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jpseverely",
    version="0.0.1",
    author="Tomoe Kuroki",
    author_email="tomokt1203@gmail.com",
    description='Package for changes in the number of covid-19 critically ill patients in Japan',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomo0503",
    project_urls={
        "Bug Tracker": "https://github.com/tomo0503",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['kotonohagetter'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'jpsev = jpsev:main'
        ]
    },
)
