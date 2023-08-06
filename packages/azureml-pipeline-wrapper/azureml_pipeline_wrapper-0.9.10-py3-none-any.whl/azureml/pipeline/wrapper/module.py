# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains classes for creating and managing resusable computational units of an Azure Machine Learning pipeline.

Modules allow you to create computational units in a :class:`azureml.pipeline.wrapper.Pipeline`, which can have
inputs, outputs, and rely on parameters and an environment configuration to operate.

Modules are designed to be reused in several pipelines and can evolve to adapt a specific computation logic
to different use cases. A step in a pipeline can be used in fast iterations to improve an algorithm,
and once the goal is achieved, the algorithm is usually published as a module to enable reuse.
"""
from azure.ml.component._module._module import Module as _Module
from azure.ml.component.component import Input as _InputBuilder, Output as _OutputBuilder, _AttrDict

Module = _Module

__all__ = [
    'Module',
    '_InputBuilder',
    '_OutputBuilder',
    '_AttrDict'
]
