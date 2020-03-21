import enum



class AccountStatus(enum.Flag):
    """Flag over set of account states.
    
    """
    NEW = enum.auto()
    FUNDING = enum.auto()
    FUNDED = enum.auto()
    ACTIVE = enum.auto()


class AccountType(enum.Enum):
    """Enumeration over set of account types.
    
    """
    CONTRACT = enum.auto()
    FAUCET = enum.auto()
    USER = enum.auto()
    BOND = enum.auto()


class BlockStatus(enum.Flag):
    """Flag over set of block states.
    
    """
    NULL = enum.auto()
    ADDED = enum.auto()
    FINALIZED = enum.auto()
    REJECTED = enum.auto()


class ContractType(enum.Enum):
    """Enumeration over set of bundled client contract types.
    
    """
    COUNTER_DEFINE = "counter_define.wasm"
    TRANSFER_U512_STORED = "transfer_to_account_u512_stored.wasm"


class DeployStatus(enum.Flag):
    """Flag over set of deploy states.
    
    """
    NULL = enum.auto()
    DISPATCHED = enum.auto()
    FINALIZED = enum.auto()
    REJECTED = enum.auto()


class DeployType(enum.Flag):
    """Flag over set of deploy types.
    
    """
    NULL = enum.auto()
    CONTRACT_INSTALL = enum.auto()
    COUNTER_CALL = enum.auto()
    TRANSFER = enum.auto()
    TRANSFER_REFUND = enum.auto()


class NetworkStatus(enum.Flag):
    """Flag over set of network states.
    
    """
    NULL = enum.auto()
    GENESIS = enum.auto()
    INITIALIZING = enum.auto()
    HEALTHY = enum.auto()
    DISTRESSED = enum.auto()
    DOWN = enum.auto()
    DE_INITIALIZING = enum.auto()


class NetworkType(enum.Enum):
    """Enumeration over set of network types.
    
    """
    LOC = enum.auto()
    DEV = enum.auto()
    LRT = enum.auto()
    SYS = enum.auto()
    STG = enum.auto()
    POC = enum.auto()
    TEST = enum.auto()
    MAIN = enum.auto()


class NodeStatus(enum.Flag):
    """Flag over set of node states.
    
    """
    NULL = enum.auto()
    GENESIS = enum.auto()
    INITIALIZING = enum.auto()
    HEALTHY = enum.auto()
    DISTRESSED = enum.auto()
    DOWN = enum.auto()
    DE_INITIALIZING = enum.auto()


class NodeType(enum.Enum):
    """Enumeration over set of node types.
    
    """
    FULL = enum.auto()
    READ_ONLY = enum.auto()


class TransferStatus(enum.Flag):
    """Flag over set of transfer states.
    
    """
    NULL = enum.auto()
    PENDING = enum.auto()
    ERROR = enum.auto()
    COMPLETE = enum.auto()


# Full set of enums.
ENUM_SET = {
    AccountStatus,
    AccountType,    
    BlockStatus,
    ContractType,
    DeployStatus,
    DeployType,
    ContractType,
    NetworkStatus,
    NetworkType,
    NodeStatus,
    NodeType,
    TransferStatus,
}
