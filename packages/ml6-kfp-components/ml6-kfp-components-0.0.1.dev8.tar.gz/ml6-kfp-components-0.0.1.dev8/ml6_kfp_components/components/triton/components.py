from kfp.v2 import dsl
from kfp.v2.dsl import Artifact, Input, Model, Output


@dsl.component(base_image="python:3.8-slim")
def AddModelToTritonRepoOp(
    model_artifact: Input[Model],
    model_config: Input[Artifact],
    model: Output[Model],
    model_repo: str,
    model_name: str,
    model_version: int,
    model_subdir: str = "",
):
    """
    A kfp component function for adding a model artifact to a Triton model repository.

    Note:
        This is supposed to be used in the context of serving with
        [Triton](https://github.com/triton-inference-server/server).

    Args:
        model_artifact: model artifact to move to the triton model repository
        model_config: triton config for the model
        model: output artifact handle for the model in the triton repository
        model_repo: gcs path to the root of the target model repository
        model_name: name for the model artifact
        model_version: version under which to save the model
        model_subdir: optional sub-directory of the model under the version directory
    """
    import shutil
    from pathlib import Path

    model_artifact_uri_fuse = model_artifact.uri.replace("gs://", "/gcs/")
    model_config_uri_fuse = model_config.uri.replace("gs://", "/gcs/")
    model_repo_fuse = model_repo.replace("gs://", "/gcs/")

    config_path = Path(model_config_uri_fuse)
    model_source = Path(model_artifact_uri_fuse)

    target_path = Path(model_repo_fuse, model_name)
    if config_path.exists():
        target_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(config_path, target_path / "config.pbtxt")

    target_path = target_path / str(model_version)
    if target_path.exists():
        shutil.rmtree(target_path)

    target_path.mkdir(parents=True, exist_ok=True)
    target_path = target_path / model_subdir
    shutil.copytree(model_source, target_path, dirs_exist_ok=True)

    model.uri = model_repo
    model.metadata = model_artifact.metadata


__all__ = [
    "AddModelToTritonRepoOp",
]
