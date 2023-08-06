# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines classes for submitted pipeline runs, including classes for checking status and retrieving run details."""

from azure.ml.component.run import _Output
from azure.ml.component._module.run import Run

OutputPort = _Output
StepRun = Run
PipelineRun = Run

__all__ = [
    'OutputPort',
    'StepRun',
    'PipelineRun'
]
