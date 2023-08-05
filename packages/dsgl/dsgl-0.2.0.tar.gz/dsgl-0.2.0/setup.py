from setuptools import find_packages, setup

# Copy the README into the long_description that appears on PyPi
with open("README.md") as file:
    long_description = file.read()

# Configuration for the build
setup(
    name="dsgl",
    packages=find_packages(include=["dsgl"]),
    version="0.2.0",
    description="Library consisting of DS shortcuts and best practice functions for the Globallogic Datascience team",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={"console_scripts": ["dsgl=dsgl.cli:main"]},
    author="DS GL Team",
    license="MIT",
    install_requires=[],
    keywords=["python", "data", "science", "globallogic"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
