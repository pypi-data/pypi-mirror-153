"""
Example of how to implement python function components with custom base images.
A custom base image here is assumed to be a python images with additional dependencies.
Do not use python function components if you can to define shared utility
functions for multiple components - use yaml components instead.

Imports used within a component need to be imported within the function.
"""
from typing import NamedTuple

from kfp.v2 import dsl
from kfp.v2.dsl import Artifact, Input, Output

import ml6_kfp_components

BASE_IMAGE = f"{ml6_kfp_components.GCP_CONTAINER_REPO}/examples/custom_base_image"
TAG = ml6_kfp_components.__version__


@dsl.component(base_image=f"{BASE_IMAGE}:{TAG}")
def ExampleComponentOp(
    input_artifact: Input[Artifact], output_artifact: Output[Artifact], input_parameter: str = None
) -> NamedTuple("outputs", [("output_param", int)]):  # noqa: F821
    """A primitive examples of a lightweight component with return value.
    Return values have to be provided in form of NamedTuples, so
    they can be accessed by name in the pipeline. You need to define
    the NamedTuple for typing inline (as shown here), otherwise kfp can not pick it up.

    Args:
        input_artifact: examples input artifact
        output_artifact: examples output artifact
        input_parameter: examples input parameter

    Returns:
        A namedtuple with an example output_param
    """
    from collections import namedtuple

    # access artifact information
    print(input_artifact.uri)
    print(output_artifact.uri)

    # make use of mounted gcs
    print(input_artifact.uri.replace("gs://", "/gcs/"))

    # print input parameter
    print(input_parameter)

    # create output namedtuple for return values
    # (does not need to contain the output artifacts)
    output = namedtuple("outputs", ["output_param"])
    return output(output_param=1)


__all__ = ["ExampleComponentOp"]
