from setuptools import setup, find_packages

setup(
    name="datastructurepack-deskent",
    version="1.2.0",
    author="Deskent",
    description="Datastorage",
    install_requires=[
        'pydantic==1.9.1',
    ],
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
)
