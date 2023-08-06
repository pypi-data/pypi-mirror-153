# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml._cli import abstract_subgroup
from azureml._cli import cli_command
from azureml._cli import argument
from azureml._cli.example import Example


class ModuleSubGroup(abstract_subgroup.AbstractSubGroup):
    """This class defines the module subgroup."""

    def get_subgroup_name(self):
        """Returns the name of the subgroup.
        This name will be used in the cli command."""
        return "module"

    def get_subgroup_title(self):
        """Returns the subgroup title as string. Title is just for informative purposes, not related
        to the command syntax or options. This is used in the help option for the subgroup."""
        return "module subgroup commands (deprecated)"

    def get_subgroup_description(self):
        """Returns the subgroup description as string. This describes the command group in details
        and could be in multi-line."""
        return "Refer to https://aka.ms/moduledoc for details."

    def get_nested_subgroups(self):
        """Returns subgroups of this subgroup."""
        return super(ModuleSubGroup, self).compute_nested_subgroups(__package__)

    def get_commands(self, for_azure_cli=False):
        """ Returns commands associated at this sub-group level."""
        decorator_commands_list = super(ModuleSubGroup, self).get_commands()
        non_decorator_commands_list = [self._debug_module_run()]
        return decorator_commands_list + non_decorator_commands_list

    def _debug_module_run(self):
        """Debug a step run/module. Put this command here to support 2 debug options: debug a step run with URL;
        debug a step run with auto arg(run id, experiment name, etc.)"""
        function_path = "azureml.pipeline.wrapper._cli.module_commands#debug_module_run"

        run_id = argument.Argument("run-id", "--run-id", "-i", help="Step run id.")
        experiment_name = argument.Argument("experiment-name", "--experiment-name", "-e", help="Experiment name.")
        url = argument.Argument("url", "--url", "-u", help="Step run url.")
        target = argument.Argument(
            "target", "--target", "",
            help="Target directory to build environment, will use current working directory if not specified.")
        spec_file = argument.Argument(
            "spec-file", "--spec-file", "",
            help="The module spec file.")
        dry_run = argument.Argument(
            "dry-run", "--dry-run", "", action='store_true',
            help="Dry run.")

        examples = [
            Example(
                name="Debug a step run and store resources(inputs, outputs, snapshot) in current directory.",
                text='az ml module debug --run-id run-id --experiment-name experiment-name '
                     '--subscription-id subscription-id --resource-group resource-group '
                     '--workspace-name workspace-name',
            ),
            Example(
                name="Debug a step run and store resources(inputs, outputs, snapshot) in specified directory.",
                text='az ml module debug --url url --working_dir ./demo',
            ),
            Example(
                name="Debug module in container.",
                text='az ml module debug --spec-file spec_file '
                     '--subscription-id subscription-id --resource-group resource-group '
                     '--workspace-name workspace-name',
            )
        ]
        return cli_command.CliCommand("debug", "Debug a step run.",
                                      [run_id, experiment_name, url, target, spec_file, dry_run,
                                       argument.WORKSPACE_NAME, argument.SUBSCRIPTION_ID,
                                       argument.RESOURCE_GROUP_NAME], function_path, examples=examples)
