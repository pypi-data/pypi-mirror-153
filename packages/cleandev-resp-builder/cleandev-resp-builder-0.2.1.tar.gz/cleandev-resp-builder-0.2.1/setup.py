import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setuptools.setup(
    name="cleandev-resp-builder",
    version="0.2.1",
    author="Daniel Rodriguez Rodriguez",
    author_email="danielrodriguezrodriguez.pks@gmail.com",
    description="Module for handler errors codes in your APIS",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cleansoftware/libs/public/cleandev-resp-builder",
    project_urls={
        "Bug Tracker": "https://gitlab.com/cleansoftware/libs/public/cleandev-resp-builder/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[
        "resp_builder",
    ],
    install_requires=[
        'click==8.0.3',
        'Flask==2.0.2',
        'Jinja2==3.0.2',
        'Werkzeug==2.0.2',
        'MarkupSafe==2.0.1',
        'itsdangerous==2.0.1',
        'backports.strenum==1.1.1',
        'cleandev-config-loader==0.3.5'
    ],
    python_requires=">=3.9",
)
