import numpy as np

from qm._QmJobErrors import _handle_job_manager_error
from qm.pb.errors_pb2 import (
    MissingJobError,
    InvalidJobExecutionStatusError,
    UnknownInputStreamError,
)
from qm.pb.general_messages_pb2 import (
    Message_LEVEL_ERROR,
    Message_LEVEL_INFO,
    Message_LEVEL_WARNING,
)
from qm.logger import logger, INFO, WARN, ERROR
from qm.pb.inc_qua_pb2 import QuaProgram
from qm.pb.job_manager_pb2 import InsertInputStreamRequest


def fix_object_data_type(obj):
    if isinstance(obj, np.floating):
        return obj.item()
    else:
        return obj


_level_map = {
    Message_LEVEL_ERROR: ERROR,
    Message_LEVEL_WARNING: WARN,
    Message_LEVEL_INFO: INFO,
}


def _set_compiler_options(request, **kwargs):
    request.highLevelProgram.compilerOptions.optimizeMergeCodeExecution = (
        kwargs.get("optimize_merge_code_execution") is not False
    )
    request.highLevelProgram.compilerOptions.optimizeWriteReadCommands = (
        kwargs.get("optimize_read_write_commands") is True
    )
    request.highLevelProgram.compilerOptions.strict = (
        kwargs.get("strict", False) is True
    )

    # handle deprecated skip_optimizations (backwards compatible for future flags)
    skip_optimizations = kwargs.get("skip_optimizations", None)
    if skip_optimizations is None:
        pass
    elif type(skip_optimizations) is tuple:
        optimization_to_skip = []
        for opt in skip_optimizations:
            if type(opt) is str:
                request.highLevelProgram.compilerOptions.skipOptimizations.append(opt)
                optimization_to_skip.append(opt)
        logger.info("Skipping optimizations: " + ",".join(optimization_to_skip))
    else:
        logger.warn("skip_optimizations must be a tuple of strings")

    # handle deprecated extra_optimizations (backwards compatible for future flags)
    extra_optimizations = kwargs.get("extra_optimizations", None)
    if extra_optimizations is None:
        pass
    elif type(extra_optimizations) is tuple:
        optimization_to_add = []
        for opt in extra_optimizations:
            if type(opt) is str:
                request.highLevelProgram.compilerOptions.skipOptimizations.append(
                    "!" + opt
                )
                optimization_to_add.append(opt)
        logger.info("extra optimizations: " + ",".join(optimization_to_add))
    else:
        logger.warn("extra_optimizations must be a tuple of strings")

    try:
        flags_arg = kwargs.get("flags", [])
        flags = [opt for opt in flags_arg if type(opt) is str]
    except TypeError:
        flags = []
    for opt in flags:
        request.highLevelProgram.compilerOptions.flags.append(opt)
    logger.info("Flags: " + ",".join(flags))


def insert_input_stream_to_job(job, data, input_stream):
    if not job._qmm._caps.supports_input_stream:
        raise Exception("`insert_input_stream()` is not supported by the QOP version.")
    request = InsertInputStreamRequest()
    request.jobId = job._id
    input_stream = input_stream.unwrap()
    if isinstance(input_stream, QuaProgram.ArrayVarRefExpression):
        request.streamName = input_stream.name
    elif (
        isinstance(input_stream, QuaProgram.AnyScalarExpression)
        and input_stream.WhichOneof("expression_oneof") == "variable"
    ):
        request.streamName = input_stream.variable.name
    else:
        raise RuntimeError(
            "Unsupported type for the input stream. Only input streams declared in the QUA program can be used."
        )
    if not isinstance(data, list):
        data = [data]
    if isinstance(data[0], int):
        request.intStreamData.data.extend(data)
        request.intStreamData.SetInParent()
    elif isinstance(data[0], float):
        request.fixedStreamData.data.extend(data)
        request.fixedStreamData.SetInParent()
    elif isinstance(data[0], bool):
        request.boolStreamData.data.extend(data)
        request.boolStreamData.SetInParent()
    response = job._job_manager_client.InsertInputStream(request)
    valid_errors = (
        MissingJobError,
        InvalidJobExecutionStatusError,
        UnknownInputStreamError,
    )
    _handle_job_manager_error(request, response, valid_errors)
