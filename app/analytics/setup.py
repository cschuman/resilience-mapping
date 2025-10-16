from setuptools import setup, find_packages

setup(
    name="resilience-analytics",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scipy>=1.9.0",
        "scikit-learn>=1.1.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.12.0",
        "geopandas>=0.12.0",
        "folium>=0.14.0",
        "statsmodels>=0.13.0",
    ],
)
