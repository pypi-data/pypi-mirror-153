import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jpsuicide",
    version="0.0.3",
    author="reo nakadate",
    author_email="s2022061@stu.musashino-u.ac.jp",
    description="A package for visualizing number of suicides in Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Reo-Nakadate/jpsuicide",
    project_urls={
        "Bug Tracker": "https://github.com/Reo-Nakadate/jpsuicide",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['jpsuicide'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'jpsuicide = jpsuicide:main'
        ]
    },
)
