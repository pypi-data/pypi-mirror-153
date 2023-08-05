from typing import NamedTuple

from kfp.v2.dsl import Artifact, Input, Output


class ExampleComponentOutput(NamedTuple):
    output_param: int


def example_component_func(
    input_artifact: Input[Artifact], output_artifact: Output[Artifact], input_parameter: str = None
) -> ExampleComponentOutput:
    """A primitive examples component.

    Args:
        input_artifact: examples input artifact
        output_artifact: examples output artifact
        input_parameter: examples input parameter

    Returns:
        A namedtuple with an examples output_param
    """
    # access artifact information
    print(input_artifact.uri)
    print(output_artifact.uri)

    # make use of mounted gcs
    print(input_artifact.uri.replace("gs://", "/gcs/"))

    # print input parameter
    print(input_parameter)

    # create output namedtuple for return values
    # (does not need to contain the output artifacts)
    return ExampleComponentOutput(output_param=1)
