import dataclasses
import typing

from stests.core.types.chain.account import Account
from stests.core.types.infra.enums import NodeStatus
from stests.core.types.infra.enums import NodeType
from stests.core.types.infra.network import NetworkIdentifier



@dataclasses.dataclass
class Node:
    """Encpasulates information pertaining to a node within a target network.
    
    """
    # Bonding account associated with node.
    account: typing.Optional[Account]

    # Node's host address.
    host: str

    # Numerical index to distinguish between nodes, e.g. node-01, node-02 ...etc.
    index: int

    # Network with which node is associated.
    network: str

    # Node's external facing GRPC port.
    port: int

    # Current node status.
    status: NodeStatus

    # Type of node in terms of it's degree of consensus participation.
    typeof: NodeType
    
    @property
    def address(self):
        return f"{self.host}:{self.port}"

    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def is_operational(self):
        return self.status in (NodeStatus.HEALTHY, NodeStatus.DISTRESSED)

    @property
    def label(self):
        return f"{self.network}:{self.index}"


@dataclasses.dataclass
class NodeIdentifier:
    """Encpasulates information required to disambiguate between nodes.
    
    """ 
    # Associated network identifer.
    network: NetworkIdentifier

    # Node index.
    index: int
 
    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"

    @property
    def label(self):
        return f"{self.network.name}:{self.label_index}"


@dataclasses.dataclass
class NodeMonitoringLock:
    """Encpasulates information used to lock monitoring of a node.
    
    """
    # Numerical index to distinguish between nodees upon the same network.
    index: int

    # Associated network.
    network: str

    # Numerical index to distinguish between multiple locks.
    lock_index: int

    @property
    def label_index(self):
        return f"N-{str(self.index).zfill(4)}"
