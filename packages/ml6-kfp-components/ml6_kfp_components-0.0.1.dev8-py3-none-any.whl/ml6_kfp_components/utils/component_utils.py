"""Utilities for component loading."""

from pathlib import Path

from jinja2 import Template
from kfp import components as comp


def load_yaml_component(component_path: str, **kwargs):
    """Loads a Kubeflow reusable component.

    Args:
        component_path: The path of the component.yaml.jinja template
        kwargs: the jinja variable values used for rendering the template

    Returns:
        A Kubeflow ContainerOp constructed from component.yaml file
    """
    if not Path(component_path).is_absolute():
        component_path = Path.cwd() / component_path
    with open(component_path, "r", encoding="utf-8") as handle:
        component_text = Template(handle.read()).render(**kwargs)

    return comp.load_component_from_text(component_text)
