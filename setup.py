from setuptools import setup, find_packages

setup(
    name="data-processor",
    version="1.0.0",
    description="A robust data processing and analysis toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.21.0",
    ],
    python_requires=">=3.9",
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-benchmark>=4.0.0",
            "pylint>=2.15.0",
            "black>=23.0.0",
            "psutil>=5.9.0",
        ]
    },
)