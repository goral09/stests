import dataclasses
import typing
from datetime import datetime

from stests.core.types.chain.enums import BlockStatus

    

@dataclasses.dataclass
class Block:
    """A block proposed/finialized within the lifetime of a chain.
    
    """
    # Block hash (blake2b) identifier.
    block_hash: str

    # Motes spent during block processing.
    deploy_cost_total: str

    # Number of deploys within block.
    deploy_count: str

    # Average price of deploys.
    deploy_gas_price_avg: int

    # J-rank.
    j_rank: int

    # Main rank.
    m_rank: int

    # Associated network.
    network: str

    # Index of node queried to pull block info.
    node_index: str

    # Size in bytes of block.
    size_bytes: int

    # Block consensus status, e.g. ADDED | FINALIZED ... etc.
    status: BlockStatus

    # Block processing timestamp.
    timestamp: datetime

    # Validator identifier that proposed block.
    validator_id: str

    @property
    def hash(self):
        return self.block_hash

    @property
    def label_j_rank(self):
        return f"{str(self.j_rank).zfill(7)}"

    @property
    def label_m_rank(self):
        return f"{str(self.m_rank).zfill(7)}"


@dataclasses.dataclass
class BlockLock:
    """Execution lock information - block.
    
    """
    # Block hash (blake2b) identifier.
    block_hash: str

    # Type of event for which the lock is being acquired.
    event_type: str

    # Associated network.
    network: str


@dataclasses.dataclass
class BlockStatistics:
    """Encapsulates statistical information pertaining to a block.
    
    """
    # Block hash (blake2b) identifier.
    block_hash: str

    # Name of chain emitting block.
    chain_name: str

    # Motes spent during block processing.
    deploy_cost_total: str

    # Number of deploys within block.
    deploy_count: str

    # Average price of deploys.
    deploy_gas_price_avg: int

    # J-rank.
    j_rank: int

    # Main rank.
    m_rank: int

    # A random bit set by the creator of the block which is goes towards the leader seed.
    magic_bit: int

    # Highway specific role of a message.
    message_role: str

    # Associated network.
    network: str

    # Address of node which emitted finalization event of the block in which deploy was included.
    node: typing.Optional[str]

    # Identifier of consensus round during which block was finalized.
    round_id: typing.Optional[int]

    # Size in bytes of block.
    size_bytes: int

    # Block consensus status, e.g. ADDED | FINALIZED ... etc.
    status: BlockStatus

    # Block processing timestamp.
    timestamp: datetime

    # ID of validator that proposed block.
    validator_id: str
