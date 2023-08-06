[TOC]

# Intro

This is a simple `test_client_class` for `flask` that I wrote to make the rest APIs created
with `openapi-python-client` work with the `flask.test_client()`s when one is writing unittests

It is a bit hacky, but it is also only meant to be used for unittests. 

# Example

In the example I am using `OpenAPI` (`flask_openapi3`), because it creates an endpoint with a json-file there can be used by `openapi_python_client` to create the rest-api which is used to call the flask application through the test client.

```python
import json
import flask
from pydantic import BaseModel, Field
from flask_openapi3 import OpenAPI


app = OpenAPI(__name__)


class SumResponse(BaseModel):
    the_sum: int = Field(..., description="sum of 2 numbers")

    
class NumbersRequest(BaseModel):
    no_1: int = Field(..., description="1st number")
    no_2: int = Field(..., description="2nd number")


@app.post(rule="/multiply-2-numbers", responses={"200": SumResponse})
def multiply_2_numbers(body: NumbersRequest):
    resp = flask.Response(json.dumps({"the_sum": body.no_1 * body.no_2}))
    resp.headers.set('Content-Type', 'application/json')
    resp.status_code = 200
    return resp


import unittest
class Testing(unittest.TestCase):
    
    def test_10_generate_rest_lib(self):
        from pathlib import Path
        from openapi_python_client import GeneratorData, Config, Project, MetaType

        config = Config()
        with app.test_client() as client:
            resp = client.get("/openapi/openapi.json")
            openapi = GeneratorData.from_dict(data=resp.json, config=config)

            path = Path(__file__).parent.joinpath("test_rest_api")
            path.mkdir(exist_ok=True)
            project = Project(openapi=openapi, meta=MetaType.NONE, config=config)
            project.package_dir = path
            project.project_dir = path
            project.update()

    def test_20_generate_rest_lib(self):
        from test_rest_api.api.default.multiply_2_numbers_multiply_2_numbers_post import (
            sync_detailed as rest_api_multiply_2_numbers)
        from test_rest_api.models.numbers_request import (
            NumbersRequest as RestApiNumbersRequest)
        from flask_httpx_request_converted_to_flask_test_client_request import ConvertHttpx2FlaskTestClient

        app.test_client_class = ConvertHttpx2FlaskTestClient

        with app.test_client() as client:
            resp = rest_api_multiply_2_numbers(client=client,
                                               json_body=RestApiNumbersRequest(no_1=42, no_2=1337))
            assert 200 == resp.status_code
            result = resp.parsed
            assert 56154 == result.the_sum

if __name__ == '__main__':
    ts = unittest.TestSuite()
    ts.addTests([
        Testing.test_10_generate_rest_lib, 
        Testing.test_20_generate_rest_lib],
    )
    
    ttr = unittest.TextTestRunner(verbosity=2)
    ttr.run(ts)

```
