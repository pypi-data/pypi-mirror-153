import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scco2",
    version="0.0.3",
    author="ryosuke yamano",
    author_email="s2022035@stu.musashino-u.ac.jp",
    description="A package for visualizing the relationship between CO2 emissions and population in a specified country",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YamanoRyosuke/scco2.py",
    project_urls={
        "Bug Tracker":"https://github.com/YamanoRyosuke/scco2.py",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['scco2'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'scco2 = scco2:main'
        ]
    },
)
