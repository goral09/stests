from datetime import datetime

from stests.core.types.infra import Network
from stests.core.types.infra import NetworkIdentifier
from stests.core.types.infra import NetworkStatus
from stests.core.types.infra import NetworkType
from stests.core.types.infra import Node
from stests.core.types.infra import NodeIdentifier
from stests.core.types.infra import NodeEventInfo
from stests.core.types.infra import NodeEventType
from stests.core.types.infra import NodeMonitoringLock
from stests.core.types.infra import NodeStatus
from stests.core.types.infra import NodeType



def create_network(name_raw: str) -> Network:
    """Returns a domain object instance: Network.
    
    """
    identifier = create_network_id(name_raw)

    return Network(
        faucet=None,
        index=identifier.index,
        name=identifier.name,
        name_raw=name_raw,
        status=NetworkStatus.HEALTHY,
        typeof=identifier.type
    )


def create_network_id(name_raw: str) -> NetworkIdentifier:
    """Returns a cache identifier: NetworkIdentifier.
    
    """
    # If name has already been parsed.
    if name_raw.upper() == name_raw:
        return NetworkIdentifier(name_raw)

    # Parse raw name.
    name_raw = name_raw.lower()
    for network_type in [i.name.lower() for i in NetworkType]:
        if name_raw.startswith(network_type):
            index=int(name_raw[len(network_type):])
            typeof=name_raw[:len(network_type)].upper()
            name = f"{typeof}-{str(index).zfill(2)}"
            return NetworkIdentifier(name=name)

    raise ValueError("Network identifier is unsupported")


def create_node(
    host: str,
    index: int,
    network_id: NetworkIdentifier,
    port: int,
    typeof: NodeType,
    status=NodeStatus.HEALTHY
    ) -> Node:
    """Returns a domain object instance: Node.
    
    """
    return Node(
        account=None,
        host=host,
        index=index,
        network=network_id.name,
        port=port,
        status=status,
        typeof=typeof
    )


def create_node_id(network_id: NetworkIdentifier, index: int) -> NodeIdentifier:
    """Returns a cache identifier: NodeIdentifier.
    
    """
    return NodeIdentifier(network_id, index)


def create_node_monitoring_lock(node_id: NodeIdentifier, lock_index: int) -> NodeMonitoringLock:
    """Returns a domain object instance: NodeMonitoringLock.
    
    """
    return NodeMonitoringLock(
        network=node_id.network.name,
        index=node_id.index,
        lock_index=lock_index,
        )


def create_node_event_info(
    node: Node,
    event_id: int,
    event_type: NodeEventType,
    block_hash: str = None,
    deploy_hash: str = None,
    ) -> NodeEventInfo:
    """Returns a domain object instance: NodeMonitoringLock.
    
    """
    return NodeEventInfo(
        block_hash=block_hash,
        deploy_hash=deploy_hash,
        event_id=event_id,
        event_ts=datetime.now(),
        event_type=event_type,
        network=node.network,
        node=node.index,
        )
