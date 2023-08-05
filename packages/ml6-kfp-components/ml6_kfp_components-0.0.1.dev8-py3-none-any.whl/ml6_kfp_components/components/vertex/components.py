from typing import NamedTuple, Optional

from kfp.v2 import dsl
from kfp.v2.dsl import Artifact, Input, Metrics, Model, Output


@dsl.component(base_image="python:3.8-slim")
def AddServingConfigOp(
    model: Input[Model],
    configured_model: Output[Artifact],
    serving_config: dict,
):
    """
    A kfp component function for adding a serving config to the metadata of a `Model` artifact.

    Note:
        The serving config is a dictionary of the form:
        ```serving_config={"containerSpec": container_spec}```

        The `containerSpec` follows:
        [ModelContainerSpec](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/ModelContainerSpec).

        Optionally the config can contain a `predictSchemata` key following:
        [PredictSchema](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/PredictSchemata).

        The reasoning here is, that the
        [ModelUploadOp](https://github.com/kubeflow/pipelines/blob/master/components/
        google-cloud/google_cloud_pipeline_components/aiplatform/model/upload_model/component.yaml)
        from `google_cloud_pipeline_components` expects this information in the artifact's metadata.

    Args:
        model: input Model artifact to which to add the serving config.
        configured_model: output Model artifact with the added serving configuration.
        serving_config: serving config to add to model

    """
    from copy import copy

    configured_model.uri = model.uri
    configured_model.metadata = copy(model.metadata)
    configured_model.metadata.update(serving_config)


@dsl.component(base_image="python:3.8-slim")
def UpdateWorkerPoolSpecsOp(
    worker_pool_specs: list,
    image_uri: Optional[str] = None,
    command: Optional[list] = None,
    args: Optional[dict] = None,
    hyperparams: Optional[dict] = None,
    env: Optional[dict] = None,
) -> list:
    """
    A kfp component function for updating the `ContainerSpecs` of a list of `WorkerPoolSpecs`.

    Note:
        For details refer to
        [ContainerSpecs](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#ContainerSpec)
        and
        [WorkerPoolSpecs](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/CustomJobSpec#WorkerPoolSpec).

    Args:
        worker_pool_specs: provided list of `WorkerPoolSpecs`
        image_uri: imageUri to add to `ContainerSpec` in each `WorkerPoolSpec`
        command: command to add to `ContainerSpec` in each `WorkerPoolSpec`
        args: args to add `ContainerSpec` args in each `WorkerPoolSpec`
        hyperparams: additional args to add to `ContainerSpec` args in each `WorkerPoolSpec`
        env: env variables to add in `ContainerSpec` env in each `WorkerPoolSpec`

    Returns:
        list of updated WorkerPoolSpecs
    """
    for spec in worker_pool_specs:
        if "container_spec" not in spec:
            spec["container_spec"] = {}

        if image_uri:
            spec["container_spec"]["image_uri"] = image_uri

        if command:
            spec["container_spec"]["command"] = command

        if args or hyperparams:
            if "args" not in spec["container_spec"]:
                spec["container_spec"]["args"] = []
            if args:
                for k, v in args.items():
                    spec["container_spec"]["args"].append(f"--{k.replace('_', '-')}={v}")
            if hyperparams:
                for k, v in hyperparams.items():
                    spec["container_spec"]["args"].append(f"--{k.replace('_', '-')}={v}")

        if env:
            if "env" not in spec["container_spec"]:
                spec["container_spec"]["env"] = []
            for k, v in env.items():
                spec["container_spec"]["env"].append(dict(name=k, value=v))

    return worker_pool_specs


@dsl.component(
    base_image="python:3.8-slim",
    packages_to_install=[
        "google-cloud-pipeline-components==1.0.4",
    ],
)
def GetCustomJobResultsOp(
    model: Output[Model],
    checkpoints: Output[Artifact],
    metrics: Output[Metrics],
    project: str,
    location: str,
    job_resource: str,
    job_id_subdir: bool = False,
):
    """
    A kfp component function for extracting `CustomTrainingJob` results.

    Note:
        This component assumes that you used the
        [CustomTrainingJobOp](https://github.com/kubeflow/pipelines/blob/master/
        components/google-cloud/google_cloud_pipeline_components/experimental/custom_job/component.yaml)
        of Google Cloud's `google_cloud_pipeline_components` package. It outputs a job_resource,
        which is used here to extract the results of the job and output respective Artifacts.
        The `CustomTrainingJobOp` in particular requires a `base_output_directory`, to which
        all the job outputs are saved.

        The following assumptions are made for the script executed in `CustomTrainingJob`:

        - the trained model artifacts is saved to `base_output_directory/model/`
        - the training checkpoints are saved to `base_output_directory/checkpoints/`
        - the training metrics are written to `base_output_directory/metrics/metadata.json`
        - artifact metadata can be written to a metadata.json in the respective directory

        If `job_id_subdir` is True, the artifacts are expected under
        `base_output_directory/<job_id>` respectively.

    Args:
        model: the model output artifact
        checkpoints: the checkpoints output artifact
        metrics: the metrics output artifact
        project: the project in which the training job was run
        location: the region in which the training job was run
        job_resource: job resource output of `CustomTrainingJobOp`
        job_id_subdir: boolean flag to indicate whether outputs are written to <job_id> subdirectory

    """
    import json
    from pathlib import Path

    import google.cloud.aiplatform as aip
    from google.protobuf.json_format import Parse
    from google_cloud_pipeline_components.proto.gcp_resources_pb2 import GcpResources

    aip.init(project=project, location=location)

    training_gcp_resources = Parse(job_resource, GcpResources())
    custom_job_id = training_gcp_resources.resources[0].resource_uri
    split_idx = custom_job_id.find("project")
    custom_job_name = custom_job_id[split_idx:]
    job = aip.CustomJob.get(custom_job_name)

    job_resource = job.gca_resource
    job_base_dir = job_resource.job_spec.base_output_directory.output_uri_prefix
    if job_id_subdir:
        job_base_dir = f"{job_base_dir}/{job.name}"

    job_base_dir_fuse = Path(job_base_dir.replace("gs://", "/gcs/"))

    artifact_mapping = dict(model=model, checkpoints=checkpoints, metrics=metrics)

    for name, artifact in artifact_mapping.items():
        uri_fuse = job_base_dir_fuse / name

        if (uri_fuse / "metadata.json").exists():
            with open(uri_fuse / "metadata.json") as fh:
                metadata = json.load(fh)
            artifact.metadata.update(metadata)

        artifact.uri = str(uri_fuse).replace("/gcs/", "gs://")


@dsl.component(
    base_image="python:3.8-slim",
    packages_to_install=[
        "google-cloud-pipeline-components==1.0.4",
    ],
)
def GetHyperparameterTuningJobResultsOp(
    trials: Output[Artifact],
    project: str,
    location: str,
    job_resource: str,
    study_spec_metrics: list,
    job_id_subdir: bool = False,
) -> NamedTuple("outputs", [("best_params", dict)]):  # noqa: F821
    """
    A kfp component function for extracting `HyperparameterTuningJob` results.

    Note:
        This component assumes that you used the
        [HyperparameterTuningJobRunOp](https://github.com/kubeflow/pipelines/blob/master/components/
        google-cloud/google_cloud_pipeline_components/experimental/hyperparameter_tuning_job/component.yaml)
        of Google Cloud's `google_cloud_pipeline_components` package. It outputs a job_resource,
        which is used here to extract the results of the job and extract the best hyperparameters.
        The `HyperparameterTuningJobRunOp` in particular requires a `base_output_directory`,
        to which the outputs of the trials are saved. If `job_id_subdir` is True, the artifacts
        are expected under `base_output_directory/<job_id>` respectively.

        The `study_spec_metrics` is defined as a
        [MetricSpec](https://cloud.google.com/vertex-ai/docs/reference/rest/v1/StudySpec#MetricSpec).

    Args:
        trials: trials output artifact handle
        project: GCP project id in which the job was run
        location: GCP location in which the job was run
        job_resource: job resource output of `HyperparameterTuningJobRunOp`
        study_spec_metrics: the studies `MetricSpec` of the `HyperparameterTuningJobRunOp`
        job_id_subdir: boolean flag to indicate whether outputs are written to <job_id> subdirectory

    Returns:
        best_params: A dictionary of the best hyperparameters
    """
    import google.cloud.aiplatform as aip
    from google.cloud.aiplatform_v1.types import study
    from google.protobuf.json_format import Parse
    from google_cloud_pipeline_components.proto.gcp_resources_pb2 import GcpResources

    aip.init(project=project, location=location)

    gcp_resources_proto = Parse(job_resource, GcpResources())
    tuning_job_id = gcp_resources_proto.resources[0].resource_uri
    split_idx = tuning_job_id.find("project")
    tuning_job_name = tuning_job_id[split_idx:]

    job = aip.HyperparameterTuningJob.get(tuning_job_name)
    job_resource = job.gca_resource
    job_base_dir = job_resource.trial_job_spec.base_output_directory.output_uri_prefix
    if job_id_subdir:
        job_base_dir = f"{job_base_dir}/{job.name}"

    trials.uri = job_base_dir

    if len(study_spec_metrics) > 1:
        raise RuntimeError(
            "Unable to determine best parameters for multi-objective hyperparameter tuning."
        )

    metric = study_spec_metrics[0]["metric_id"]
    goal = study_spec_metrics[0]["goal"]
    if goal == study.StudySpec.MetricSpec.GoalType.MAXIMIZE:
        best_fn = max
        goal_name = "maximize"
    else:
        best_fn = min
        goal_name = "minimize"
    best_trial = best_fn(
        job_resource.trials, key=lambda trial: trial.final_measurement.metrics[0].value
    )

    trials.metadata = dict(
        metric=metric,
        goal=goal_name,
        num_trials=len(job_resource.trials),
        best_metric_value=best_trial.final_measurement.metrics[0].value,
    )

    from collections import namedtuple

    output = namedtuple("outputs", ["best_params"])
    return output(best_params={p.parameter_id: p.value for p in best_trial.parameters})


__all__ = [
    "AddServingConfigOp",
    "UpdateWorkerPoolSpecsOp",
    "GetCustomJobResultsOp",
    "GetHyperparameterTuningJobResultsOp",
]
