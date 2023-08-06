from setuptools import setup, find_packages
import os.path as path

long_desc = open(path.join(path.dirname(__file__), "README.md")).read()

setup(
    name="grade-tracker",
    version="2.0.0",
    author="Dan Walters",
    author_email="dan.walters5@outlook.com",
    description="A CLI to track grades",
    url="https://github.com/dwdwdan/grade-tracker",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["xdg", "pyyaml"],
    entry_points={
        "console_scripts": [
                "grade-tracker=grade_tracker.cli:main",
            ]
        },
    long_description=long_desc,
    long_description_content_type="text/markdown",
)
