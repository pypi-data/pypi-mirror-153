from pathlib import Path

from kfp.v2.dsl import Artifact, Model

from ml6_kfp_components.components.vertex import AddServingConfigOp


def test_add_serving_config(tmp_path: Path) -> None:
    model_name = "model"
    model_uri = "model-uri"
    model_metadata = dict(framework="tf")

    configured_model_name = "configured-model"

    model = Model(uri=model_uri, name=model_name, metadata=model_metadata)
    configured_model = Artifact(name=configured_model_name)

    serving_config = dict(containerSpec=dict(imageUri="test-image-uri"))

    _ = AddServingConfigOp.python_func(
        model=model, configured_model=configured_model, serving_config=serving_config
    )

    # check that the input model is unchanged
    assert model.name == model_name
    assert model.uri == model_uri
    assert model.metadata == model_metadata

    # check that the output configured model get the input model name
    # and uri and has the serving config in its metadata
    assert configured_model.name == configured_model_name
    assert configured_model.uri == model.uri
    assert configured_model.metadata.get("framework") == model_metadata["framework"]
    assert configured_model.metadata.get("containerSpec") == serving_config["containerSpec"]
