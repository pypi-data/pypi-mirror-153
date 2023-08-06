# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""A wrapper to analyze function annotations, generate module specs, and run module in command line."""
from azure.ml.component._util._exceptions import TooManyDSLComponentsError, RequiredParamParsingError
from azure.ml.component.dsl import _component
from azure.ml.component.dsl._component import ComponentExecutor
from azure.ml.component.dsl.types import Input as InputPath
from azure.ml.component.dsl.types import _InputFile as InputFile
from azure.ml.component.dsl.types import Output as OutputPath
from azure.ml.component.dsl.types import _OutputFile as OutputFile
from azure.ml.component.dsl.types import String as StringParameter
from azure.ml.component.dsl.types import Enum as EnumParameter
from azure.ml.component.dsl.types import Integer as IntParameter
from azure.ml.component.dsl.types import Float as FloatParameter
from azure.ml.component.dsl.types import Boolean as BoolParameter

TooManyDSLModulesError = TooManyDSLComponentsError
ModuleExecutor = ComponentExecutor

ModuleExecutor.collect_module_from_file = ComponentExecutor.collect_component_from_file
ModuleExecutor.collect_module_from_py_module = ComponentExecutor.collect_component_from_py_module
ModuleExecutor.collect_modules_from_py_module = ComponentExecutor.collect_components_from_py_module

InputDirectory = InputPath
OutputDirectory = OutputPath


def module(
    name=None, version='0.0.1', namespace=None,
    description=None,
    is_deterministic=None,
    tags=None, contact=None, help_document=None,
    os=None,
    base_image=None, conda_dependencies=None,
    custom_image=None,
):
    """Return a decorator which is used to declare a module with @dsl.module.

    :param name: The name of the module. If None is set, camel cased function name is used.
    :type name: str
    :param description: The description of the module. If None is set, the doc string is used.
    :type description: str
    :param version: Version of the module.
    :type version: str
    :param namespace: Namespace of the module.
    :type namespace: str
    :param is_deterministic: Specify whether the component will always generate the same result.
    :type is_deterministic: bool
    :param tags: Tags of the module.
    :type tags: builtin.list
    :param contact: Contact of the module.
    :type contact: str
    :param help_document: Help document of the module.
    :type help_document: str
    :param os: OS type of the module.
    :type os: str
    :param base_image: Base image of the module.
    :type base_image: str
    :param conda_dependencies: Dependencies of the module.
    :type conda_dependencies: str
    :param custom_image: User provided docker image, if it is not None, the module will directly run with the image,
                         user should take care of preparing all the required dependent packages in the image.
                         in this case, both base_image and conda_dependencies should be None.
    :type custom_image: str
    :return: An injected function which could be passed to ModuleExecutor
    """
    display_name = name
    if namespace and name is None:
        raise ValueError("When namespace is not None, name cannot be None.")
    if name:
        name = name if namespace is None else '%s.%s' % (namespace, name)
        name = name.lower().replace('/', '.').replace(' ', '_')
    tags = {key: None for key in tags} if tags else {}
    if help_document:
        tags['helpDocument'] = help_document
    if contact:
        tags['contact'] = contact
    tags['codegenBy'] = 'dsl.module'
    return _component(
        name=name, version=version, display_name=display_name,
        description=description, is_deterministic=is_deterministic,
        tags=tags, os=os,
        base_image=base_image, conda_dependencies=conda_dependencies,
        custom_image=custom_image,
    )


__all__ = [
    'RequiredParamParsingError',
    'TooManyDSLModulesError',
    'ModuleExecutor',
    'InputPath',
    'InputDirectory',
    'OutputDirectory',
    'InputFile',
    'OutputPath',
    'OutputFile',
    'StringParameter',
    'EnumParameter',
    'IntParameter',
    'FloatParameter',
    'BoolParameter',
]
