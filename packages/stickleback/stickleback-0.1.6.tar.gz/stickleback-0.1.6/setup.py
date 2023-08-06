import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="stickleback",
    version="0.1.6",
    description="Automated behavioral event detection in bio-logging data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="http://github.com/FlukeAndFeather/stickleback",
    author="Max Czapanskiy",
    author_email="maxczapanskiy@gmail.com",
    license="MIT",
    packages=['stickleback'],
    include_package_data=True,
    package_data={'stickleback': ['data/*']},
    install_requires=[
            "jupyter",
            "matplotlib",
            "numpy >=1.21.0, <1.22",
            "pandas",
            "plotly",
            "scikit-learn",
            "scipy",
            "sktime >=0.11"
        ]
)
