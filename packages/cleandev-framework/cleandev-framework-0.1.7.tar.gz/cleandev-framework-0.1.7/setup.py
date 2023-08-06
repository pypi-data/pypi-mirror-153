import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="cleandev-framework",
    version="0.1.7",
    author="Daniel Rodriguez Rodriguez",
    author_email="danielrodriguezrodriguez.pks@gmail.com",
    description="Adaptadores de modelos de base de datos",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cleansoftware/libs/public/cleandev-framework",
    project_urls={
        "Bug Tracker": "https://gitlab.com/cleansoftware/libs/public/cleandev-framework/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[
        "cleandev_framework"
    ],
    install_requires=[
        'cleandev-config-loader==0.3.5',
        'cleandev-generic-utils==0.1.9',
        'cleandev-validator==0.3.1',
        'cleandev-postgresql-db==0.3.6'
    ],
    python_requires=">=3.9",
)
