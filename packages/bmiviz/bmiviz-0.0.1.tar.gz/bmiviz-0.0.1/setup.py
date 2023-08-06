import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bmiviz",
    version="0.0.1",
    author="shotaro yoshimura",
    author_email="shotaro.yoshimura.mdchor@gmail.com",
    description="A package for visualizing BMI trend of each country",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MDchor/BMI-visualisation",
    project_urls={
        "Bug Tracker": "https://github.com/MDchor/BMI-visualisation",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['bmiviz'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'bmiviz = bmiviz:main'
        ]
    },
)
