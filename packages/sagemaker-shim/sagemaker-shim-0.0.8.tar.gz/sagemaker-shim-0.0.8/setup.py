# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sagemaker_shim', 'sagemaker_shim.vendor', 'sagemaker_shim.vendor.werkzeug']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'click', 'fastapi', 'uvicorn[standard]']

entry_points = \
{'console_scripts': ['sagemaker-shim = sagemaker_shim.cli:cli']}

setup_kwargs = {
    'name': 'sagemaker-shim',
    'version': '0.0.8',
    'description': 'Adapts algorithms that implement the Grand Challenge inference API for running in SageMaker',
    'long_description': '# SageMaker Shim for Grand Challenge\n\n[![CI](https://github.com/jmsmkn/sagemaker-shim/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jmsmkn/sagemaker-shim/actions/workflows/ci.yml?query=branch%3Amain)\n[![PyPI](https://img.shields.io/pypi/v/sagemaker-shim)](https://pypi.org/project/sagemaker-shim/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sagemaker-shim)](https://pypi.org/project/sagemaker-shim/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis repo contains a library that adapts algorithms that implement the Grand Challenge inference API for running in SageMaker.\n\nThe application contains:\n\n- A `click` cli client with options to launch a web server\n- A `fastapi` web server that implements the SageMaker endpoints\n- and `pydantic` models that interface between S3, and run the original inference jobs.\n\nThe application is compiled on Python 3.10 using `pyinstaller`, and then distributed as a statically linked binary using `staticx`.\nIt is able to adapt any container, including ones based on `scratch` or `alpine` images.\n\n## Usage\n\nThe binary is designed to be added to an existing container image that implements the Grand Challenge API.\nOn Grand Challenge this happens automatically by using [crane](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_mutate.md) to add the binary, directories and environment variables to each comtainer image.\nThe binary itself will:\n\n1. Download the input files from the provided locations on S3 to `/input`, optionally decompressing the inputs.\n1. Execute the original container program in a subprocess.\n   This is found by inspecting the following environment variables:\n    - `GRAND_CHALLENGE_COMPONENT_CMD_B64J`: the original `cmd` of the container, json encoded as a base64 string.\n    - `GRAND_CHALLENGE_COMPONENT_ENTRYPOINT_B64J`: the original `entrypoint` of the container, json encoded as a base64 string.\n1. Upload the contents of `/output` to the given output S3 bucket and prefix.\n\n### `sagemaker-shim serve`\n\nThis starts the webserver on http://0.0.0.0:8080 which implements the [SageMaker API](https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-batch-code.html).\nThere are three endpoints:\n\n- `/ping` (GET): returns an empty 200 response if the container is healthy\n- `/execution-parameters` (GET): returns the preferred execution parameters for AWS SageMaker Batch Inference\n- `/invocations` (POST): SageMaker can make POST requests to this endpoint.\n  The body contains the json encoded data required to run a single inference task:\n\n  ```json\n    {\n        "pk": "unique-test-id",\n        "inputs": [\n            {\n                "relative_path": "interface/path",\n                "bucket_name": "name-of-input-bucket",\n                "bucket_key": "/path/to/input/file/in/bucket",\n                "decompress": false,\n            },\n            ...\n        ],\n        "output_bucket_name": "name-of-output-bucket",\n        "output_prefix": "/prefix/of/output/files",\n    }\n  ```\n\n  The endpoint will return an object containing the return code of the subprocess in `response["return_code"]`,\n  and any outputs will be placed in the output bucket at the output prefix.\n\n### Patching an Existing Container\n\nTo patch an existing container image in a registry see the example in [tests/utils.py](tests/utils.py).\nFirst you will need to get the original `cmd` and `entrypoint` using `get_new_env_vars` and `get_image_config`.\nThen you can add the binary, set the new `cmd`, `entrypoint`, and environment variables with `mutate_image`.\n',
    'author': 'James Meakin',
    'author_email': '12661555+jmsmkn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DIAGNijmegen/rse-sagemaker-shim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
