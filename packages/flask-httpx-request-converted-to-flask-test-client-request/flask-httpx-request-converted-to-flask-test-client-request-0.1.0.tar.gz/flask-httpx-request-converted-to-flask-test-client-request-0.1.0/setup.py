import setuptools
import flask_httpx_request_converted_to_flask_test_client_request

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="flask-httpx-request-converted-to-flask-test-client-request",
    version=flask_httpx_request_converted_to_flask_test_client_request.__version__,
    author="Dennis Vestergaard Værum",
    author_email="convert_httpx_2_flask_test_client@varum.dk",
    license="0BSD",
    description="Unittest Tool: This is a `flask.test_client_class` I wrote to making the libraries created by "
                "`openapi-python-client` work with `flask.test_client()`",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dvaerum/flask-httpx-request-converted-to-flask-test-client-requests",
    packages=["flask_httpx_request_converted_to_flask_test_client_request"],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
