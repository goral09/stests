import typing

from casperlabs_client.abi import ABI

from stests.core import cache
from stests.core.clx import utils
from stests.core.logging import log_event
from stests.core.types.chain import Account
from stests.core.types.infra import Node
from stests.core.types.chain import ContractType
from stests.core.types.orchestration import ExecutionContext
from stests.events import EventType



# Type of contract.
TYPE = ContractType.TRANSFER_U512_STORED

# Wasm file name.
WASM = "transfer_to_account_u512_stored.wasm"

# Entry point when calling into contract.
_SESSION_ENTRY_POINT = "transfer"

# Name of contract - see use when passed as session-name.
_NKEY = "transfer_to_account"

# Named keys associated with contract.
NKEYS = [
    _NKEY,
]


def install(src: typing.Any, account: Account) -> typing.Tuple[Node, str, float, int]:
    """Installs a smart contract under an account.

    :param src: The source from which a node client will be instantiated.
    :param account: Account under which contract will be installed.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts).

    """
    return utils.install_contract_by_hash(src, account, WASM)


def transfer(ctx: ExecutionContext, cp1: Account, cp2: Account, amount: int) -> typing.Tuple[Node, str, float, int]:
    """Executes a transfer between 2 counter-parties & returns resulting deploy hash.

    :param ctx: Execution context information.
    :param cp1: Account information of counter party 1.
    :param cp2: Account information of counter party 2.
    :param amount: Amount in motes to be transferred.

    :returns: 4 member tuple -> (node, deploy_hash, dispatch_duration, dispatch_attempts).

    """
    # Set named key associated with contract.
    named_key = cache.infra.get_named_key(ctx.network, TYPE, _NKEY)
    if named_key is None:
        raise ValueError(f"{WASM} has not been installed upon chain.")

    # Dispatch deploy.
    node, _, deploy_hash, dispatch_duration, dispatch_attempts = utils.dispatch_deploy(
        src=ctx,
        account=cp1,
        session_entry_point=_SESSION_ENTRY_POINT,
        session_hash=named_key.hash_as_bytes,
        session_args=ABI.args([
            ABI.account("target", cp2.account_id),
            ABI.big_int("amount", amount),
            ]),
    )

    log_event(EventType.MONITORING_DEPLOY_DISPATCHED, f"TRANSFER_U512_STORED {amount} CLX from {cp1.public_key[:8]} to {cp2.public_key[:8]}", node, deploy_hash=deploy_hash)

    return node, deploy_hash, dispatch_duration, dispatch_attempts
