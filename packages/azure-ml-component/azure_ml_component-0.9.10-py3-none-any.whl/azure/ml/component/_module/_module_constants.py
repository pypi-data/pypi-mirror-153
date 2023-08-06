# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
PARAMETERS = 'parameters'
OUTPUTS = 'outputs'
INPUTS = 'inputs'
IGNORE_PARAMS = {
    # FixedParams
    'ServingEntry', 'Target', 'MLCComputeType', 'PrepareEnvironment',
    'Script', 'Framework', 'MaxRunDurationSeconds', 'InterpreterPath',
    'UserManagedDependencies', 'CondaDependencies', 'DockerEnabled', 'BaseDockerImage',
    'GpuSupport', 'HistoryEnabled', 'Arguments',
    # MPI, TODO confirm
    'Communicator', 'MpiProcessCountPerNode', 'NodeCount',
}
