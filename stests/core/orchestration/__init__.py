from stests.core.orchestration.enums import *
from stests.core.orchestration.identifiers import *
from stests.core.orchestration.context import *
from stests.core.orchestration.info import *
from stests.core.orchestration.locks import *
from stests.core.orchestration.state_history import *


# from stests.core.orchestration.phase import *
# from stests.core.orchestration.run import *
# from stests.core.orchestration.step import *



# Set of supported classes.
DCLASS_SET = {
    PhaseLock,
    PhaseState,
    RunIdentifier,
    ExecutionContext,
    RunInfo,
    RunLock,
    RunState,
    StepLock,
    StepState,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | ENUM_SET
