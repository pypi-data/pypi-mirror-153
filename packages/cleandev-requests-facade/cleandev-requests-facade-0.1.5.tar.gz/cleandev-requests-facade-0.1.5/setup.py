import setuptools
import pathlib

HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="cleandev-requests-facade",
    version="0.1.5",
    author="Daniel Rodriguez Rodriguez",
    author_email="danielrodriguezrodriguez.pks@gmail.com",
    description="Fachada para autenticación de JWT",
    long_description=README,
    long_description_content_type="text/markdown",

    url="https://gitlab.com/cleansoftware/libs/public/cleandev-req-facade",
    project_urls={
        "Bug Tracker": "https://gitlab.com/cleansoftware/libs/public/cleandev-req-facade/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['requests_facade'],
    install_requires=[
        'requests==2.27.1',
        'backports.strenum==1.1.1',
        'cleandev-config-loader==0.3.5',
        'cleandev-generic-utils==0.1.9'
    ],
    python_requires=">=3.9",
)

