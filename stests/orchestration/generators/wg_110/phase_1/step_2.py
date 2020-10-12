import typing
import datetime 
import dramatiq

from stests.core.types.infra import NodeIdentifier
from stests.core.types.orchestration import ExecutionContext
from stests.orchestration.generators.utils import constants
from stests.orchestration.generators.utils import verification
from stests.orchestration.generators.utils.accounts import do_transfer_wasm as do_transfer



# Step label.
LABEL = "fund-run-accounts"


def execute(ctx: ExecutionContext) -> typing.Union[dramatiq.Actor, int, typing.Callable]:
    """Step entry point.
    
    :param ctx: Execution context information.

    :returns: 3 member tuple -> actor, message count, message arg factory.

    """
    def _yield_parameterizations() -> typing.Generator:
        for account_index in range(ctx.args.transfers):
            yield (
                ctx,
                constants.ACC_NETWORK_FAUCET,
                account_index,
                ctx.args.amount,
            )

    return do_transfer, ctx.args.transfers, _yield_parameterizations


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    verification.verify_deploy_count(ctx, ctx.args.transfers) 
