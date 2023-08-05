"""
Example yaml based component.
This directory can contain multiple yaml based components.
Note that these components are based on the container image defined in this directory.
They can have shared utility code.
"""
from pathlib import Path

import ml6_kfp_components
from ml6_kfp_components.utils.component_utils import load_yaml_component

BASE_IMAGE = f"{ml6_kfp_components.GCP_CONTAINER_REPO}/example/yaml_based"
TAG = ml6_kfp_components.__version__

ExampleComponentOp = load_yaml_component(
    component_path=str(Path(__file__).parent / "example_component.jinja.yaml"),
    base_image=BASE_IMAGE,
    tag=TAG,
)

__all__ = ["ExampleComponentOp"]
