# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml._cli.cli_command import command
from azureml._cli import argument
from azureml._cli.example import Example

from azure.ml.component._cli.component_commands import CLIModule, _debug_module
from azureml.pipeline.wrapper._cli.module_subgroup import ModuleSubGroup

NAMESPACE = argument.Argument(
    "namespace", "--namespace", "", required=False,
    help="Namespace of the module.")
MODULE_NAME = argument.Argument(
    "module_name", "--name", "-n", required=True,
    help="Name of the module.")
MODULE_VERSION = argument.Argument(
    "module_version", "--version", "-v", required=False,
    help="Version of the module.")

_DEFAULT_NAMESPACE_CONFIG_KEY = 'module_namespace'


def _literal_boolean(s):
    return s.lower() != 'false'


@command(
    subgroup_type=ModuleSubGroup,
    command="register",
    short_description="Create or upgrade a module.",
    long_description="Modules could either be registered from a local folder, a GitHub url, "
                     "or a zip package (typically created by a DevOps CI build job).",
    argument_list=[
        argument.Argument(
            "spec_file", "--spec-file", "-f", required=False,
            help="The module spec file. Accepts either a local file path, a GitHub url, "
                 "or a relative path inside the package specified by --package-zip."),
        argument.Argument(
            "package_zip", "--package-zip", "-p", required=False,
            help="The zip package contains the module spec and implemention code. "
                 "Currently only accepts url to a DevOps build drop."),
        argument.Argument(
            "set_as_default", "--set-as-default-version", "-a", action="store_true", required=False,
            help="By default, default version of the module will not be updated "
                 "when registering a new version of module. "
                 "Specify this flag to set the new version as the module's default version."),
        argument.Argument(
            "amlignore_file", "--amlignore-file", "-i", required=False,
            help="The .amlignore or .gitignore file used to exclude files/directories in the snapshot."),
        argument.Argument(
            "fail_if_exists", "--fail-if-exists", "", action="store_true", required=False,
            help="By default, the CLI exits as succeed (exit 0) if the same version of module "
                 "already exists in workspace. "
                 "Specify this flag to exit as failure (exit non-zero) for the case."),
        argument.Argument(
            "version", "--set-version", "", required=False,
            help="If specified, registered module's version will be overwritten to specified value "
                 "instead of the version in the yaml."),
    ],
    examples=[
        Example(
            name="Register from local folder",
            text="az ml module register --spec-file=path/to/module_spec.yaml",
        ),
        Example(
            name="Register a new version of an existing module",
            text="az ml module register --spec-file=path/to/new/version/of/module_spec.yaml",
        ),
        Example(
            name="By default, registering a new version will not update the default version "
                 "of the module. Use --set-as-default-version to update the default version",
            text="az ml module register --spec-file=path/to/new/version/of/module_spec.yaml --set-as-default-version",
        ),
        Example(
            name="Register from GitHub url",
            text="az ml module register --spec-file=https://github.com/user/repo/path/to/module_spec.yaml",
        ),
        Example(
            name="Register from a zip package build by DevOps",
            text="az ml module register --package-zip=https://dev.azure.com/path/to/the/module_package.zip "
                 "--spec-file=module_spec.yaml",
        ),
        Example(
            name="Register from local folder with .amlignore",
            text="az ml module register --spec-file=path/to/module_spec.yaml --amlignore-file path/to/.amlignore",
        ),
        Example(
            name="Register from local folder with specific version number",
            text="az ml module register --spec-file=path/to/module_spec.yaml --set-version xx.xx.xx",
        ),
        Example(
            name="Register all modules inside .moduleproject",
            text="az ml module register --spec-file=path/to/.moduleproj",
            # TODO: add a user manual for .moduleproj here
        ),
    ])
def register_module(
        workspace=None,
        spec_file=None,
        package_zip=None,
        set_as_default=False,
        amlignore_file=None,
        fail_if_exists=False,
        version=None,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return cli_module.register(
        spec_file=spec_file,
        package_zip=package_zip,
        set_as_default=set_as_default,
        amlignore_file=amlignore_file,
        fail_if_exists=fail_if_exists,
        version=version)


@command(
    subgroup_type=ModuleSubGroup,
    command="validate-spec",
    short_description="Validate module spec file.",
    long_description="Validate module spec before registering to a workspace.\n\n"
                     "The spec file could either located in a local folder or a GitHub url.",
    argument_list=[
        argument.Argument(
            "spec_file", "--spec-file", "-f", required=False,
            help="The module spec file. Accepts either a local file path, a GitHub url, "
                 "or a relative path inside the package specified by --package-zip."),
        argument.Argument(
            "package_zip", "--package-zip", "-p", required=False,
            help="The zip package contains the module spec and implemention code. "
                 "Currently only accepts url to a DevOps build drop."),
    ],
    examples=[
        Example(
            name="Validate module spec located in a local folder",
            text="az ml module validate-spec --spec-file=path/to/module_spec.yaml",
        ),
        Example(
            name="Validate module spec located in a GitHub repo",
            text="az ml module validate-spec --spec-file=https://github.com/user/repo/path/to/module_spec.yaml",
        ),
        Example(
            name="Validate module spec located inside a package zip",
            text="az ml module validate-spec --package-zip=https://dev.azure.com/path/to/the/module_package.zip "
                 "--spec-file=module_spec.yaml",
        ),
    ])
def validate(
        workspace=None,
        spec_file=None,
        package_zip=None,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return cli_module.validate(
        spec_file=spec_file,
        package_zip=package_zip,
    )


@command(
    subgroup_type=ModuleSubGroup,
    command="list",
    short_description="List modules in a workspace.",
    argument_list=[
        argument.Argument(
            "include_disabled", "--include-disabled", "", action="store_true", required=False,
            help="Include disabled modules in list result."),
    ],
    examples=[
        Example(
            name="Show module list as table",
            text="az ml module list --output table",
        ),
        Example(
            name="List both active and disabled modules in a workspace",
            text="az ml module list --include-disabled",
        ),
    ])
def list_modules(
        workspace=None,
        include_disabled=False,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return [r for r in cli_module.list(
        include_disabled=include_disabled
    )]


@command(
    subgroup_type=ModuleSubGroup,
    command="show",
    short_description="Show detail information of a module.",
    argument_list=[
        NAMESPACE,
        MODULE_NAME,
        MODULE_VERSION,
    ],
    examples=[
        Example(
            name="Show detail information of a module's default version",
            text='az ml module show --name "Module Name"',
        ),
        Example(
            name="Show detail information of a module's specific version",
            text='az ml module show --name "Module Name" --version 0.0.1',
        ),
        Example(
            name="Show detail information of a module within specific namespace",
            text='az ml module show --name "Module Name" --namespace microsoft.com/azureml/samples',
        ),
    ])
def show_module(
        workspace=None,
        namespace=None,
        module_name=None,
        module_version=None,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return cli_module.show(
        namespace=namespace,
        module_name=module_name,
        component_version=module_version,
    )


@command(
    subgroup_type=ModuleSubGroup,
    command="enable",
    short_description="Enable a module.",
    argument_list=[
        NAMESPACE,
        MODULE_NAME,
    ],
    examples=[
        Example(
            name="Enable a module",
            text='az ml module enable --name "Module Name"',
        ),
        Example(
            name="Enable a module within specific namespace",
            text='az ml module enable --name "Module Name" --namespace microsoft.com/azureml/samples',
        ),
    ])
def enable_module(
        workspace=None,
        namespace=None,
        module_name=None,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return cli_module.enable(
        namespace=namespace,
        module_name=module_name,
    )


@command(
    subgroup_type=ModuleSubGroup,
    command="disable",
    short_description="Disable a module.",
    argument_list=[
        NAMESPACE,
        MODULE_NAME,
    ],
    examples=[
        Example(
            name="Disable a module",
            text='az ml module disable --name "Module Name"',
        ),
        Example(
            name="Disable a module within specific namespace",
            text='az ml module disable --name "Module Name" --namespace microsoft.com/azureml/samples',
        ),
    ])
def disable_module(
        workspace=None,
        namespace=None,
        module_name=None,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return cli_module.disable(
        namespace=namespace,
        module_name=module_name,
    )


@command(
    subgroup_type=ModuleSubGroup,
    command="set-default-version",
    short_description="Set default version of a module.",
    long_description="By default, registering a new version to an existing module will not update "
                     "the default version of the module. This is useful for a module to be registered for testing.\n\n"
                     "When the tests passed and ready to ship, use this command to update the default version to "
                     "the new version of the module.\n\n"
                     "Also this command could be used to revert a module's version in case when some bugs "
                     "has been detected in the production environment.",
    argument_list=[
        NAMESPACE,
        MODULE_NAME,
        argument.Argument("module_version", "--version", "-v", required=True,
                          help="Version to be set as default."),
    ],
    examples=[
        Example(
            name="Set default version of a module",
            text='az ml module set-default-version --name "Module Name" --version 0.0.1',
        ),
        Example(
            name="Set default version of a module within specific namespace",
            text='az ml module set-default-version --name "Module Name" --namespace microsoft.com/azureml/samples',
        ),
    ])
def set_module_default_version(
        workspace=None,
        namespace=None,
        module_name=None,
        module_version=None,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return cli_module.set_default_version(
        namespace=namespace,
        module_name=module_name,
        module_version=module_version,
    )


@command(
    subgroup_type=ModuleSubGroup,
    command="download",
    short_description="Download a module to a specified directory.",
    argument_list=[
        NAMESPACE,
        MODULE_NAME,
        MODULE_VERSION,
        argument.Argument(
            "target_dir", "--target-dir", "",
            help="The target directory to save to. Will use current working directory if not specified."),
        argument.Argument(
            "overwrite", "--overwrite", "-y", action="store_true",
            help="Overwrite if the target directory is not empty.")
    ],
    examples=[
        Example(
            name="Download component spec along with the snapshot to current working directory",
            text='az ml module download --name "Module Name"',
        ),
        Example(
            name="Download module to a specific folder",
            text='az ml module download --name "Module Name" --target-dir path/to/save',
        ),
        Example(
            name="Download module of specific version",
            text='az ml module download --name "Module Name" --version 0.0.1',
        )
    ])
def download_module(
        workspace=None,
        namespace=None,
        module_name=None,
        module_version=None,
        target_dir=None,
        overwrite=None,
        logger=None):
    cli_module = CLIModule(workspace, logger)
    return cli_module.download(
        namespace=namespace,
        module_name=module_name,
        component_version=module_version,
        target_dir=target_dir,
        overwrite=overwrite
    )


@command(
    subgroup_type=ModuleSubGroup,
    command="init",
    short_description="Add a dsl.module entry file and resources into a pipeline project.",
    argument_list=[
        argument.Argument(
            "source", "--source", "",
            help="Source used to init the module, could be pacakge.function or path/to/python_file.py "
                 "or path/to/python_file.ipynb."),
        argument.Argument(
            "module_name", "--name", "-n",
            help="Name of the module."),
        argument.Argument(
            "job_type", "--type", "", default='basic', choices=['basic', 'mpi', 'parallel'],
            help="Job type of the module. Could be basic, mpi."),
        argument.Argument(
            "source_dir", "--source-dir", "",
            help="Source directory to init the environment, "
                 "resources(notebook, data, test) will be generated under source directory, "
                 "will be os.cwd() if not set. "
                 "Note when init a module from scratch, a new folder will be generated under source directory. "
                 "Source directory will be that folder in this case."),
        argument.Argument(
            "inputs", "--inputs", "", nargs='+',
            help="Input names of the module when init from an argparse entry"),
        argument.Argument(
            "outputs", "--outputs", "", nargs='+',
            help="Output names of the module when init from an argparse entry"),
        argument.Argument(
            "entry_only", "--entry-only", "", action='store_true',
            help="If specified, only module entry will be generated."),
    ],
    examples=[
        Example(
            name="Create a simple module from template with name \"Sample Module\" in sample_module folder.",
            text="az ml module init --name \"Sample Module\"",
        ),
        Example(
            name="Create an mpi module from template with name \"Sample MPI Module\" in sample_mpi_module folder.",
            text="az ml module init --name \"Sample MPI Module\" --type mpi",
        ),
        Example(
            name="Create a simple module from template with name \"Sample Module\" in folder my_folder/sample_module. "
                 "Note source directory here is my_folder/sample_module instead of my_folder.",
            text="az ml module init --name \"Sample Module\" --source-dir my_folder",
        ),
        Example(
            name="Create a module from existing function 'add' in 'my_module.py' in folder add.",
            text="az ml module init --source my_module.add"
        ),
        Example(
            name="Create a module from existing function 'add' in 'my_module.py' and use name \"My Add\" in "
                 "folder my_add.",
            text="az ml module init --source my_module.add --name \"My Add\""
        ),
        Example(
            name="Create a module from an existing python entry 'main.py' in which argparse is used,"
                 " inputs are input1, input2, outputs are output1, output2.",
            text="az ml module init --source main.py --inputs input1 input2 --outputs output1 output2"
        ),
        Example(
            name="Create a module from an existing jupyter notebook entry 'main.ipynb'.",
            text="az ml module init --source main.ipynb"
        ),
        Example(
            name="Create resources from existing dsl.module, source directory would be entry_folder. "
                 "Note the source file's location relative to current folder is entry_folder/sample_module.py",
            text="az ml module init --source sample_module.py --source-dir entry_folder"
        ),
        Example(
            name="Create resources from existing dsl.module, source directory would be current folder.",
            text="az ml module init --source my_modules.my_module"
        ),
        Example(
            name="Create a simple module entry with name \"Sample Module\" in sample_module folder.",
            text="az ml module init --name \"Sample Module\" --entry-only"
        )
    ])
def init_module(
        source=None,
        module_name=None,
        job_type=None,
        source_dir=None,
        inputs=None,
        outputs=None,
        entry_only=None,
        logger=None):
    cli_module = CLIModule(None, logger)
    return cli_module.init(
        source=source,
        component_name=module_name,
        job_type=job_type,
        source_dir=source_dir,
        inputs=inputs,
        outputs=outputs,
        entry_only=entry_only
    )


@command(
    subgroup_type=ModuleSubGroup,
    command="build",
    short_description="Builds dsl.module into module spec.",
    argument_list=[
        argument.Argument(
            "target", "--target", "",
            help="Target module project or module file. Will use current working directory if not specified."),
        argument.Argument(
            "source_dir", "--source-dir", "",
            help="Source directory to build spec, will be os.cwd() if not set.")
    ],
    examples=[
        Example(
            name="Build all dsl.modules in module_folder into specs.",
            text="az ml module build --target module_folder",
        ),
        Example(
            name="Build a dsl.module file into spec.",
            text="az ml module build --target module.py",
        ),
        Example(
            name="Build a dsl.module file into spec, spec file will be generated in 'entry_folder', "
                 "source directory will be current folder.",
            text="az ml module build --target entry_folder/module.py"
        ),
        Example(
            name="Build a dsl.module file into spec, source directory will be 'a/b', "
                 "spec file will be generated in 'entry_folder'.",
            text="az ml module build --target a/b/c/module.py --source-dir a/b"
        ),
        Example(
            name="Build all modules inside .moduleproject",
            text="az ml module build --target=path/to/.moduleproj",
            # TODO: add a user manual for .moduleproj here
        )
    ])
def build_module(
        target=None,
        source_dir=None,
        logger=None):
    cli_module = CLIModule(None, logger)
    return cli_module.build(
        target=target,
        source_dir=source_dir
    )


def debug_module_run(
        run_id=None,
        experiment_name=None,
        url=None,
        target=None,
        spec_file=None,
        dry_run=None,
        subscription_id=None, resource_group_name=None, workspace_name=None):
    return _debug_module(
        run_id=run_id,
        experiment_name=experiment_name,
        url=url,
        target=target,
        spec_file=spec_file,
        dry_run=dry_run,
        subscription_id=subscription_id, resource_group_name=resource_group_name, workspace_name=workspace_name
    )
