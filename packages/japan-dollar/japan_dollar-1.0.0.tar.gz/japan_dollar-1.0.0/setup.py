import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="japan_dollar",
    version="1.0.0",
    author="Sota Chira",
    description="A package for visualizing bilateral import between Japan and any country",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/noboru-knm/World-Trade-Visualization",
    project_urls={
        "Bug Tracker": "https://github.com/noboru-knm/World-Trade-Visualization",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['japan_dollar'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'japan_dollar = japan_dollar:main'
        ]
    },
)
