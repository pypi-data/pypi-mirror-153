# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import sys
import logging
import argparse

from azure.ml.component._debug._step_run_debugger import OnlineStepRunDebugger, _setup_debug
from azure.ml.component.dsl._graph_2_code._code_generator import _generate_package, _compare_package,\
    PipelinePackageGenerator, PipelinePackageCompare
from azure.ml.component._util._loggerfactory import _LoggerFactory


_logger = _LoggerFactory.get_logger("az-ml")


def _set_workspace_argument_for_subparsers(subparser):
    subparser.add_argument(
        '--subscription_id', '-s', type=str,
        help="Subscription id, required when pass run id."
    )
    subparser.add_argument(
        '--resource_group', '-r', type=str,
        help="Resource group name, required when pass run id."
    )
    subparser.add_argument(
        '--workspace_name', '-w', type=str,
        help="Workspace name, required when pass run id."
    )

    subparser.add_argument(
        '--debug', action="store_true",
        help="Increase logging verbosity to show all debug logs"
    )


def _set_common_argument_for_subparsers(subparser):
    _set_workspace_argument_for_subparsers(subparser)
    subparser.add_argument(
        '--path', '-p', type=str,
        help="Path to export the pipeline to. If not specified, default will be set."
    )
    subparser.add_argument(
        '--include-components', type=str,
        help="""Included components to download snapshot.
        * to export all components;
        ',' separated string which contains a subset of components
        """
    )


def _entry(argv):
    """
    CLI tool to export UI graph to Component SDK code, compare codes of two pipelines
    or debug component using common-runtime.
    """
    parser = argparse.ArgumentParser(
        prog="az-ml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A CLI tool to export UI graph to Component SDK code, "
                    "compare codes of two pipelines or debug component using common-runtime."
    )

    subparsers = parser.add_subparsers()

    # az-ml export
    export_parser = subparsers.add_parser(
        'export',
        description='A CLI tool to export UI graph to Component SDK code.',
        help='az-ml export'
    )
    _set_common_argument_for_subparsers(export_parser)
    export_parser.add_argument(
        '--pipeline-run', type=str,
        help="ID of the Pipeline Run to export (guid)."
    )
    export_parser.add_argument(
        '--url', type=str,
        help="URL of the Pipeline run/draft/endpoint to export."
    )
    export_parser.set_defaults(classname=PipelinePackageGenerator)

    # az-ml compare
    compare_parser = subparsers.add_parser(
        'compare',
        description='A CLI tool to export UI graph to Component SDK code and compare codes of two pipelines.',
        help='az-ml compare'
    )
    _set_common_argument_for_subparsers(compare_parser)
    compare_parser.add_argument(
        'pipeline1', type=str,
        help="First URL of the Pipeline Run to export, and URL recommended to be enclosed in double quotes in cmd."
    )
    compare_parser.add_argument(
        'pipeline2', type=str,
        help="Second URL of the Pipeline Run to export, and URL recommended to be enclosed in double quotes in cmd"
    )
    compare_parser.set_defaults(classname=PipelinePackageCompare)

    # az-ml run debug
    run_parser = subparsers.add_parser(
        "run", description='A CLI tool to local debug component using common-runtime.',
        help='az-ml run').add_subparsers()
    local_debug_parser = run_parser.add_parser(
        "debug",
        description='A CLI tool to local debug using common runtime.',
        help='az-ml run debug'
    )
    _set_workspace_argument_for_subparsers(local_debug_parser)
    local_debug_parser.add_argument(
        "--run-id", type=str,
        help="The run id of step run to be debugged."
    )
    local_debug_parser.set_defaults(classname=OnlineStepRunDebugger)

    args = parser.parse_args(argv)

    if args.debug:
        for log_handler in _logger.handlers:
            if isinstance(log_handler, logging.StreamHandler):
                log_handler.setLevel(logging.DEBUG)

    if args.classname == PipelinePackageGenerator:
        _generate_package(
            url=args.url,
            subscription_id=args.subscription_id,
            resource_group=args.resource_group,
            workspace_name=args.workspace_name,
            run_id=args.pipeline_run,
            include_components=args.include_components,
            target_dir=args.path,
        )

    elif args.classname == PipelinePackageCompare:
        _compare_package(
            run_item1=args.pipeline1,
            run_item2=args.pipeline2,
            subscription_id=args.subscription_id,
            resource_group=args.resource_group,
            workspace_name=args.workspace_name,
            include_components=args.include_components,
            target_dir=args.path,
        )
    elif args.classname == OnlineStepRunDebugger:
        common_runtime_debug_args = {"compute": "local", "runtime": "common", **vars(args)}
        _setup_debug(common_runtime_debug_args)


def az_ml_cli():
    """Use as a CLI entry function to use ComponentProject."""
    _entry(sys.argv[1:])
