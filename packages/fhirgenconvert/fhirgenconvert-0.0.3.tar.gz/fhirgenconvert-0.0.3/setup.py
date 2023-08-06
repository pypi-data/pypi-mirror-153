'''Setup file for fhirgenconvert package'''
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fhirgenconvert",
    version="0.0.3",
    author="Elizabeth Shivers",
    author_email="elizabeth.shivers@gtri.gatech.edu",
    description="A companion package for FHIR Generator to convert struture definitions to class wrappers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SmartChartSuite/FHIRGenConvert",
    project_urls={
        "Bug Tracker": "https://github.com/SmartChartSuite/FHIRGenConvert/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    entry_points={
        'console_scripts': ['fhirgenconvert=src.fhirgenconvert:main']
    }
)
