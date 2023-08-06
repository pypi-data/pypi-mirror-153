# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml._cli import abstract_subgroup
from azureml._cli import cli_command
from azureml._cli import argument
from azureml._cli.example import Example
import argparse

COMPONENT_SET = argument.Argument(
    "set", "--set", "", required=False, nargs=argparse.ONE_OR_MORE,
    help="Create or Update an object by specifying a property path and value to set. "
         "Example: --set property1.property2=<value>.")
COMPONENT_NAME_OPTIONAL = argument.Argument(
    "component_name", "--name", "", required=False,
    help="Name of the component.")
COMPONENT_NAME = COMPONENT_NAME_OPTIONAL.get_required_true_copy()
COMPONENT_VERSION = argument.Argument(
    "component_version", "--version", "", required=False,
    help="Version of the component.")
LABEL = argument.Argument(
    "label", "--label", "", required=False,
    help="A label is an alias for certain component version. "
         "Specify label to \"default\" to set current version as the component's default version. "
         "If not specified, default version will remain unchanged. "
)
SELECTOR = argument.Argument(
    "selector", "--selector", "", required=False,
    help="The selector can just be a name, or it can be a name with a version or a label, "
         "such as mycomponent:0.7.1 or mycomponent@beta. If no label or version is provided, "
         "the version with the label @default will be chosen. If no version has the @default label, "
         "then the version with the @latest label will be chosen. "
         "Note if version is specified both in version and selector, version in selector will be applied."
)
# TODO: rename argument name to file
FILE = argument.Argument(
    "spec_file", "--file", "", required=False,
    help="The component spec file. Accepts either a local file path or a GitHub url")
AML_IGNORE_FILE = argument.Argument(
    "amlignore_file", "--amlignore-file", "", required=False,
    help="The .amlignore or .gitignore file used to exclude files/directories in the snapshot.")


class ComponentSubGroup(abstract_subgroup.AbstractSubGroup):
    """This class defines the component sub group."""

    def get_subgroup_name(self):
        """Returns the name of the subgroup.
        This name will be used in the cli command."""
        return "component"

    def get_subgroup_title(self):
        """Returns the subgroup title as string. Title is just for informative purposes, not related
        to the command syntax or options. This is used in the help option for the subgroup."""
        return "component subgroup commands (preview)"

    def get_subgroup_description(self):
        """Get detailed description when calling az ml component -h."""
        return 'Reference https://aka.ms/component-cli-walk-through for common use cases. \n' \
               'For detailed help docs, use "az ml component command -h". ' \
               'For example: "az ml component create -h".'

    def get_nested_subgroups(self):
        """Returns sub-groups of this sub-group."""
        return super(ComponentSubGroup, self).compute_nested_subgroups(__package__)

    def get_commands(self, for_azure_cli=False):
        """ Returns commands associated at this sub-group level."""
        commands_list = [
            self._command_build(),
            self._command_create(),
            self._command_validate(),
            self._command_list(),
            self._command_show(),
            self._command_restore(),
            self._command_archive(),
            self._command_update(),
            self._command_download(),
            # Hide these commands for now
            # TODO: enable related tests when exposing them
            # self._command_component_export(),
            # self._command_init(),
            # self._command_build_spec(),
            # self._command_debug()
        ]
        return commands_list

    def _command_component_export(self):
        # Note: put export to module_commands because cli requires all handler function in same package
        function_path = "azure.ml.component._cli.component_commands#_export"

        url = argument.Argument("url", "--url", "", required=False,
                                help="url of the PipelineDraft or PipelineRun to export")
        draft_id = argument.Argument("draft_id", "--draft-id", "", required=False,
                                     help="ID of the PipelineDraft to export")
        run_id = argument.Argument("run_id", "--run-id", "", required=False,
                                   help="ID of the PipelineRun to export")
        path = argument.Argument("path", "--target", "", required=False,
                                 help="File path to save exported graph to.")
        export_format = argument.Argument("export_format", "--export-format", "", required=False,
                                          help="Export file format of the entry pipeline. One of \
                                          {py, ipynb, Python, JupyterNotebook}. Default value is JupyterNotebook",
                                          default="JupyterNotebook")
        subscription_id = argument.Argument("subscription_id", "--subscription-id", "", required=False,
                                            help="Subscription ID")
        return cli_command.CliCommand("export", "Export pipeline draft or pipeline run as sdk code",
                                      [url,
                                       draft_id,
                                       run_id,
                                       path,
                                       export_format,
                                       subscription_id,
                                       argument.RESOURCE_GROUP_NAME,
                                       argument.WORKSPACE_NAME], function_path)

    def _command_build(self):
        function_path = "azure.ml.component._cli.component_commands#_build_component_snapshot"

        arguments = [
            argument.Argument(
                "spec_file", "--file", "", required=True,
                help="The component spec file. Only local file is allowed."),
            AML_IGNORE_FILE,
            argument.Argument(
                "target_dir", "--target", "", required=False,
                help="The target directory to place built snapshot in, will clean up the directory if exist. "
                     "Note target directory will be implicitly ignored when building the snapshot.")
        ]

        examples = [
            Example(
                name="Build component snapshot from local directory",
                text="az ml component build --file path/to/component_spec.yaml",
            ),
            Example(
                name="Build component snapshot from local directory with .amlignore",
                text="az ml component build --file path/to/component_spec.yaml "
                     "--amlignore-file path/to/.amlignore",
            ),
            Example(
                name="Build component snapshot to a specific directory.",
                text="az ml component build --file path/to/component_spec.yaml --target path/to/save",
            ),
        ]

        return cli_command.CliCommand(
            name='build',
            title='Build a local snapshot of a component.',
            arguments=arguments,
            handler_function_path=function_path,
            description="By default, the built snapshot will be saved in .build directory in spec file's "
                        "code directory. Build output directory will be implicitly ignored when building the "
                        "snapshot.",
            examples=examples
        )

    def _command_create(self):
        function_path = "azure.ml.component._cli.component_commands#_create_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            FILE,
            argument.Argument(
                "package_zip", "--package", "", required=False,
                help="The zip package contains the component spec and implemention code. "
                     "Currently only accepts url to a DevOps build drop."),
            argument.Argument(
                "manifest", "--manifest", "", required=False,
                help="The relative path inside the package specified by --package."),
            LABEL,
            AML_IGNORE_FILE,
            argument.Argument(
                "fail_if_exists", "--fail-if-exists", "", action="store_true", required=False,
                help="By default, the CLI exits as succeed (exit 0) if the same version of component "
                     "already exists in workspace. "
                     "Specify this flag to exit as failure (exit non-zero) for the case."),
            argument.Argument(
                "version", "--version", "", required=False,
                help="If specified, created component's version will be overwritten to specified value "
                     "instead of the version in the yaml."),
            argument.Argument(
                "registry", "--registry", "", required=False,
                help="If specified, created registry component."),
            COMPONENT_SET
        ]

        examples = [
            Example(
                name="Create from local directory",
                text="az ml component create --file=path/to/component_spec.yaml",
            ),
            Example(
                name="Create a new version of an existing component",
                text="az ml component create --file=path/to/new/version/of/component_spec.yaml",
            ),
            Example(
                name="By default, creating a new version will not update the default version "
                     "of the component. Use --label default to update the default version",
                text="az ml component create --file=path/to/new/version/of/component_spec.yaml "
                     "--label default",
            ),
            Example(
                name="Create from GitHub url",
                text="az ml component create --file=https://github.com/user/repo/path/to/component_spec.yaml",
            ),
            Example(
                name="Create from a zip package build by DevOps",
                text="az ml component create --package=https://dev.azure.com/path/to/the/component_package.zip "
                     "--manifest=component_spec.yaml",
            ),
            Example(
                name="Create from local directory with .amlignore",
                text="az ml component create --file=path/to/component_spec.yaml "
                     "--amlignore-file path/to/.amlignore",
            ),
            Example(
                name="Create from local directory with specific version number",
                text="az ml component create --file=path/to/component_spec.yaml --version xx.xx.xx",
            ),
            Example(
                name="Create registry component from local directory",
                text='az ml component create --file=path/to/component_spec.yaml --registry "register Name"',
            ),
            Example(
                name="Create from local directory and set an object by specifying a property path and value",
                text='az ml component create --file=path/to/component_spec.yaml --set property1.property2=<value>',
            )
        ]

        return cli_command.CliCommand(
            name='create',
            title="Create a version of the component in workspace based on the provided file.",
            arguments=arguments,
            handler_function_path=function_path,
            description="Components could either be created from a local directory, a GitHub url, "
                        "or a zip package (typically created by a DevOps CI build job).",
            examples=examples
        )

    def _command_validate(self):
        function_path = "azure.ml.component._cli.component_commands#_validate_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            FILE,
            argument.Argument(
                "package_zip", "--package", "", required=False,
                help="The zip package contains the component spec and implemention code. "
                     "Currently only accepts url to a DevOps build drop."),
            argument.Argument(
                "manifest", "--manifest", "", required=False,
                help="The relative path inside the package specified by --package."),
        ]

        examples = [
            Example(
                name="Validate component spec located in a local directory",
                text="az ml component validate --file=path/to/component_spec.yaml",
            ),
            Example(
                name="Validate component spec located in a GitHub repo",
                text="az ml component validate "
                     "--file=https://github.com/user/repo/path/to/component_spec.yaml",
            ),
            Example(
                name="Validate component spec located inside a package zip",
                text="az ml component validate "
                     "--package=https://dev.azure.com/path/to/the/component_package.zip "
                     "--manifest=component_spec.yaml",
            ),
        ]

        return cli_command.CliCommand(
            name='validate',
            title='Validate the component definition in the provided file.',
            arguments=arguments,
            handler_function_path=function_path,
            description="Validate component spec before adding to a workspace.\n\n"
                        "The spec file could either located in a local directory or a GitHub url.",
            examples=examples
        )

    def _command_list(self):
        function_path = "azure.ml.component._cli.component_commands#_list_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            COMPONENT_NAME_OPTIONAL,
            argument.Argument(
                "include_disabled", "--include-archived", "", action="store_true", required=False,
                help="Include archived components in list result."),
            argument.Argument(
                "registry", "--registry", "", required=False,
                help="If specified, list registry component.")
        ]

        examples = [
            Example(
                name="Show component list as table",
                text="az ml component list --output table",
            ),
            Example(
                name="List both active and archived components in a workspace",
                text="az ml component list --include-archived",
            ),
            Example(
                name="List all versions of a component.",
                text='az ml component list --name "component Name"',
            ),
            Example(
                name="List registry component",
                text='az ml component list --registry "register Name"',
            )
        ]

        return cli_command.CliCommand(
            name='list',
            title='List components in a workspace.',
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )

    def _command_show(self):
        function_path = "azure.ml.component._cli.component_commands#_show_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            COMPONENT_NAME_OPTIONAL,
            COMPONENT_VERSION,
            SELECTOR,
            argument.Argument(
                "registry", "--registry", "", required=False,
                help="If specified, show registry component.")
        ]

        examples = [
            Example(
                name="Show detail information of a component's default version",
                text='az ml component show --name "component Name"',
            ),
            Example(
                name="Show detail information of a component's specific version",
                text='az ml component show --name "component Name" --version 0.0.1',
            ),
            Example(
                name="Show detail information of a registry component's default version ",
                text='az ml component show --name "component Name" --registry "register Name"',
            )
        ]

        return cli_command.CliCommand(
            name='show',
            title="Show the yaml representation of a component version.",
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )

    def _command_restore(self):
        function_path = "azure.ml.component._cli.component_commands#_restore_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            COMPONENT_NAME_OPTIONAL,
            SELECTOR
        ]

        examples = [
            Example(
                name="Restore a component",
                text='az ml component restore --name "component Name"',
            ),
        ]

        return cli_command.CliCommand(
            name='restore',
            title='Restore a component that was previously archived.',
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )

    def _command_archive(self):
        function_path = "azure.ml.component._cli.component_commands#_archive_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            COMPONENT_NAME_OPTIONAL,
            SELECTOR
        ]

        examples = [
            Example(
                name="Archive a component",
                text='az ml component archive --name "component Name"',
            ),
        ]

        return cli_command.CliCommand(
            name='archive',
            title="Archive a component to exclude it in list result by default.",
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )

    def _command_update(self):
        # TODO: enable update label
        function_path = "azure.ml.component._cli.component_commands#_component_update"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            COMPONENT_NAME_OPTIONAL,
            COMPONENT_VERSION,
            LABEL,
            SELECTOR,
            COMPONENT_SET
        ]

        examples = [
            Example(
                name="Set default version of a component",
                text='az ml component update --name "component Name" --version 0.0.1 --label default',
            ),
        ]

        return cli_command.CliCommand(
            name='update',
            title="Update a version of the component based on the provided file.",
            arguments=arguments,
            handler_function_path=function_path,
            description="By default, creating a new version to an existing component will not update "
                        "the default version of the component. "
                        "This is useful for a component to be created for testing.\n\n"
                        "When the tests passed and ready to ship, use this command to update the default version to "
                        "the new version of the component.\n\n"
                        "Also this command could be used to revert a component's version in case when some bugs "
                        "has been detected in the production environment.",
            examples=examples
        )

    def _command_download(self):
        function_path = "azure.ml.component._cli.component_commands#_download_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            COMPONENT_NAME_OPTIONAL,
            COMPONENT_VERSION,
            SELECTOR,
            argument.Argument(
                "target_dir", "--target", "",
                help="The target directory to save to. Will use current working directory if not specified."),
            argument.Argument(
                "overwrite", "--overwrite", "", action="store_true",
                help="Overwrite if the target directory is not empty.")
        ]

        examples = [
            Example(
                name="Download component spec along with the snapshot to current working directory",
                text='az ml component download --name "component Name"',
            ),
            Example(
                name="Download component to a specific directory",
                text='az ml component download --name "component Name" --target path/to/save',
            ),
            Example(
                name="Download component of specific version",
                text='az ml component download --name "component Name" --version 0.0.1',
            )
        ]

        return cli_command.CliCommand(
            name='download',
            title="Download snapshot of the component.",
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )

    def _command_init(self):
        function_path = "azure.ml.component._cli.component_commands#_init_component"

        arguments = [
            argument.Argument(
                "source", "--source", "",
                help="Source used to init the component, could be pacakge.function or path/to/python_file.py "
                     "or path/to/python_file.ipynb."),
            argument.Argument(
                "component_name", "--name", "",
                help="Name of the component."),
            argument.Argument(
                "job_type", "--type", "", default='basic', choices=['basic', 'mpi', 'parallel'],
                help="Job type of the component. Could be basic, mpi."),
            argument.Argument(
                "source_dir", "--source-dir", "",
                help="Source directory to init the environment, "
                     "resources(notebook, data, test) will be generated under source directory, "
                     "will be os.cwd() if not set. "
                     "Note when init a component from scratch, a new directory will be generated under "
                     "source directory. "
                     "Source directory will be that directory in this case."),
            argument.Argument(
                "inputs", "--inputs", "", nargs='+',
                help="Input names of the component when init from an argparse entry"),
            argument.Argument(
                "outputs", "--outputs", "", nargs='+',
                help="Output names of the component when init from an argparse entry"),
            argument.Argument(
                "entry_only", "--entry-only", "", action='store_true',
                help="If specified, only component entry will be generated."),
        ]

        examples = [
            Example(
                name="Create a simple component from template with name \"Sample component\" in "
                     "sample_component directory.",
                text="az ml component init --name \"Sample component\"",
            ),
            Example(
                name="Create an mpi component from template with name \"Sample MPI component\" in "
                     "sample_mpi_component directory.",
                text="az ml component init --name \"Sample MPI component\" --type mpi",
            ),
            Example(
                name="Create a simple component from template with name \"Sample component\" in directory "
                     "my_dir/sample_component. "
                     "Note source directory here is my_dir/sample_component instead of my_dir.",
                text="az ml component init --name \"Sample component\" --source-dir my_dir",
            ),
            Example(
                name="Create a component from existing function 'add' in 'my_component.py' in directory add.",
                text="az ml component init --source my_component.add"
            ),
            Example(
                name="Create a component from existing function 'add' in 'my_component.py' and use name \"My Add\" "
                     "in directory my_add.",
                text="az ml component init --source my_component.add --name \"My Add\""
            ),
            Example(
                name="Create a component from an existing python entry 'main.py' in which argparse is used,"
                     " inputs are input1, input2, outputs are output1, output2.",
                text="az ml component init --source main.py --inputs input1 input2 --outputs output1 output2"
            ),
            Example(
                name="Create a component from an existing jupyter notebook entry 'main.ipynb'.",
                text="az ml component init --source main.ipynb"
            ),
            Example(
                name="Create resources from existing dsl.component, source directory would be entry_dir. "
                     "Note the source file's location relative to current directory is entry_dir/sample_module.py",
                text="az ml component init --source sample_module.py --source-dir entry_dir"
            ),
            Example(
                name="Create resources from existing dsl.component, source directory would be current directory.",
                text="az ml component init --source my_components.my_component"
            ),
            Example(
                name="Create a simple component entry with name \"Sample component\" in sample_component directory.",
                text="az ml component init --name \"Sample component\" --entry-only"
            )
        ]

        return cli_command.CliCommand(
            name='init',
            title='Add a dsl.component entry file and resources into a component project.',
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )

    def _command_build_spec(self):
        function_path = "azure.ml.component._cli.component_commands#_build_component_spec"

        arguments = [
            argument.Argument(
                "target", "--target", "",
                help="Target component project or component file. "
                     "Will use current working directory if not specified."),
            argument.Argument(
                "source_dir", "--source-dir", "",
                help="Source directory to build spec, will be os.cwd() if not set.")
        ]

        examples = [
            Example(
                name="Build all dsl.components in component_dir into specs.",
                text="az ml component build --target component_dir",
            ),
            Example(
                name="Build a dsl.component file into spec.",
                text="az ml component build --target component.py",
            ),
            Example(
                name="Build a dsl.component file into spec, spec file will be generated in 'entry_dir', "
                     "source directory will be current directory.",
                text="az ml component build --target entry_dir/component.py"
            ),
            Example(
                name="Build a dsl.component file into spec, source directory will be 'a/b', "
                     "spec file will be generated in 'entry_dir'.",
                text="az ml component build --target a/b/c/component.py --source-dir a/b"
            ),
            Example(
                name="Build all components inside .componentproject",
                text="az ml component build --target=path/to/.componentproj",
                # TODO: add a user manual for .componentproj here
            )
        ]

        return cli_command.CliCommand(
            name='build',
            title='Builds dsl.component.',
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )

    def _command_debug(self):
        """Debug a step run/component. Put this command here to support 2 debug options: debug a step run with URL;
        debug a step run with auto arg(run id, experiment name, etc.)"""
        function_path = "azure.ml.component._cli.component_commands#_debug_component"

        arguments = [
            argument.WORKSPACE_NAME,
            argument.RESOURCE_GROUP_NAME,
            argument.SUBSCRIPTION_ID,
            argument.Argument("run-id", "--run-id", "", help="Step run id."),
            argument.Argument("experiment-name", "--experiment-name", "", help="Experiment name."),
            argument.Argument("url", "--url", "", help="Step run url."),
            argument.Argument(
                "target", "--target", "",
                help="Target directory to build environment, will use current working directory if not specified."),
            argument.Argument("spec-file", "--file", "", help="The component spec file."),
            argument.Argument("compute", "--compute", "", help="Debug component in compute."),
            argument.Argument("dry-run", "--dry-run", "", action='store_true', help="Dry run.")
        ]

        examples = [
            Example(
                name="Debug a step run and store resources(inputs, outputs, snapshot) in current directory.",
                text='az ml component debug --run-id run-id --experiment-name experiment-name '
                     '--subscription-id subscription-id --resource-group resource-group '
                     '--workspace-name workspace-name --compute local',
            ),
            Example(
                name="Debug a step run and store resources(inputs, outputs, snapshot) in specified directory.",
                text='az ml component debug --url url --target ./demo --compute local',
            ),
            Example(
                name="Debug component in container.",
                text='az ml component debug --file spec_file '
                     '--subscription-id subscription-id --resource-group resource-group '
                     '--workspace-name workspace-name',
            ),
            Example(
                name="Debug step run in remote compute.",
                text='az ml component debug --run-id run_id '
                     '--subscription-id subscription-id --resource-group resource-group '
                     '--workspace-name workspace-name --compute remote_compute_name',
            )
        ]

        return cli_command.CliCommand(
            name='debug',
            title='Debug a component.',
            arguments=arguments,
            handler_function_path=function_path,
            examples=examples
        )
