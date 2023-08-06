import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eqone",
    version="0.0.1",
    author="junya toyokura",
    author_email="j.toyokura@agreement.jp",
    description="A package for visualizing worlf earthquske for one month",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Junya-Toyokura/world-earthquake-for-one-month",
    project_urls={
        "Bug Tracker": "https://github.com/Junya-Toyokura/world-earthquake-for-one-month",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['eqone'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'eqone = eqone:main'
        ]
    },
)
