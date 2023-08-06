# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains core functionality for Azure Machine Learning pipelines, which are configurable machine learning workflows.

Azure Machine Learning pipelines allow you to create resusable machine learning workflows that can be used as a
template for your machine learning scenarios. This package contains the core functionality for working with
Azure ML pipelines.

A machine learning pipeline is represented by a :class:`azureml.pipeline.wrapper.Pipeline` object which can be
constructed for a collection of :class:`azureml.pipeline.wrapper.Module` object that can sequenced and parallelized,
or be created with explicit dependencies.

You can create and work with pipelines in a Jupyter Notebook or any other IDE with the Azure ML SDK installed.
"""

import logging

from .module import Module
from .pipeline import Pipeline
from .pipeline_run import PipelineRun, StepRun, OutputPort
from .pipeline_endpoint import PipelineEndpoint

import azure.ml.component._util._loggerfactory as ComponentLoggerFactory

# Patch the module to make it use the correct package name.
#
# NOTE: Because of the hack here, if wrapper is imported, even we use component then, the telemetry will still
#       mark everything it sends as "wrapper" package. This is not ideal. Considering that most people are unlikely to
#       have a mixed usage of wrapper & component package in real life, there should be very limited practical issues.
ComponentLoggerFactory.COMPONENT_NAME = 'azureml.pipeline.wrapper'

module_logger = logging.getLogger(__name__)
module_logger.warning("azureml.pipeline.wrapper has been deprecated, please switch to azure.ml.component. "
                      "Support of azureml-pipeline-wrapper package will end after 2021/7/31.")

__all__ = [
    'Module',
    'Pipeline',
    'PipelineRun',
    'StepRun',
    'OutputPort',
    'PipelineEndpoint'
]
