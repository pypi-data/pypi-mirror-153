import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_analyzer",
    version="0.0.1",
    license='MIT',
    author="KSV Muralidhar",
    author_email="murali_dhar0552@yahoo.com",
    description="Auto EDA package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "pandas==1.3.5",
        "numpy==1.21.6",
        "matplotlib==3.5.1",
        "seaborn==0.11.2",
        "scikit-learn==1.0.2",
        "scipy==1.7.3",
        "ipython==7.34.0",
        "statsmodels==0.13.2"
    ],
    python_requires=">=3.7"
)
