# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""A decorator which builds a :class:azureml.pipeline.wrapper.Pipeline."""

from azure.ml.component.dsl._pipeline import pipeline
from .module import module

__all__ = [
    'pipeline',
    'module'
]
