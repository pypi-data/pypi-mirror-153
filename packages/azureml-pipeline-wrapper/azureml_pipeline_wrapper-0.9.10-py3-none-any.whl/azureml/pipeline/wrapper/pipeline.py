# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the class for creating reusable Azure Machine Learning workflows."""

from azure.ml.component import Pipeline

Pipeline = Pipeline
Pipeline.run = Pipeline._run

__all__ = [
    'Pipeline'
]
