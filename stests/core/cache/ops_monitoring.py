import typing

from stests.core.cache.enums import StoreOperation
from stests.core.cache.enums import StorePartition
from stests.core.cache.utils import cache_op
from stests.core.types.chain import Block
from stests.core.types.chain import Deploy
from stests.core.types.chain import DeploySummary
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import NodeMonitoringLock


# Cache partition.
_PARTITION = StorePartition.MONITORING

# Cache collections.
COL_BLOCK = "block"
COL_DEPLOY = "deploy"
COL_NODE_LOCK = "node-lock"



@cache_op(_PARTITION, StoreOperation.DELETE)
def delete_node_monitor_lock(lock: NodeMonitoringLock) -> typing.Generator:
    """Deletes astream lock.

    :param ctx: Execution context information.

    :returns: A keypath to be deleted.
    
    """
    return [
        lock.network,
        COL_NODE_LOCK,
        lock.label_index,
        lock.lock_index,
    ]


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_block(network_id: NetworkIdentifier, block_hash: str) -> typing.List[str]:
    """Returns domain object: Block.
    
    :param block_hash: Hash of a cached block.

    :returns: Cached block information.

    """
    return [
        network_id.name,
        COL_BLOCK,
        f"*.{block_hash}"
    ]


@cache_op(_PARTITION, StoreOperation.GET_ONE)
def get_deploy(network_id: NetworkIdentifier, deploy_hash: str) -> typing.List[str]:
    """Returns domain object: Deploy.
    
    :param deploy_hash: Hash of a cached deploy.

    :returns: Cached deploy information.

    """
    return [
        network_id.name,
        COL_DEPLOY,
        f"*.{deploy_hash}"
    ]


@cache_op(_PARTITION, StoreOperation.SET_SINGLETON)
def set_block(block: Block) -> typing.Tuple[typing.List[str], Block]:
    """Encaches domain object: Block.
    
    :param block: Block domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        block.network,
        COL_BLOCK,
        f"{block.label_j_rank}.{block.block_hash}"
    ], block


@cache_op(_PARTITION, StoreOperation.SET_SINGLETON)
def set_deploy_summary(deploy_summary: DeploySummary) -> typing.Tuple[typing.List[str], DeploySummary]:
    """Encaches domain object: DeploySummary.
    
    :param deploy: Deploy domain object instance to be cached.

    :returns: Keypath + domain object instance.

    """
    return [
        deploy_summary.network,
        COL_DEPLOY,
        f"{deploy_summary.block_hash}.{deploy_summary.deploy_hash}"
    ], deploy_summary


@cache_op(_PARTITION, StoreOperation.LOCK)
def set_node_monitor_lock(lock: NodeMonitoringLock) -> typing.Tuple[typing.List[str], NodeMonitoringLock]:
    """Encaches a lock: NodeMonitoringLock.

    :param lock: Information to be locked.

    """
    return [
        lock.network,
        COL_NODE_LOCK,
        lock.label_index,
        lock.lock_index,
    ], lock
