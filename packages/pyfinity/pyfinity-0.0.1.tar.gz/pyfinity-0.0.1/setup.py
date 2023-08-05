import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfinity",
    version="0.0.1",
    author="Mahesh Maximus",
    author_email="",
    description="A tool that makes the python interpreter seamlessly run forever.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mahesh-maximus/pyfinity",
    project_urls={
        "Bug Tracker": "https://github.com/mahesh-maximus/pyfinity/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
        entry_points={
                        'console_scripts': [
                                'pyfinity=pyfinity.watchmedo:main',
                        ]
                }
)
