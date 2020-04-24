import argparse
import pathlib

from stests.core import cache
from stests.core.types.chain import AccountType
from stests.core.utils import args_validator
from stests.core.utils import crypto
from stests.core import factory
from stests.core.utils import logger



# CLI argument parser.
ARGS = argparse.ArgumentParser(f"Register a network's faucet key with stests.")

# CLI argument: network name.
ARGS.add_argument(
    "network",
    help="Network name {type}{id}, e.g. lrt1.",
    type=args_validator.validate_network
    )

# Set CLI argument: private key in PEM format.
ARGS.add_argument(
    "pem_path",
    help="Absolute path to the faucet private key in PEM format.",
    type=args_validator.validate_filepath
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """    
    # Pull.
    network = cache.infra.get_network_by_name(args.network)
    if network is None:
        raise ValueError("Unregistered network.")

    # Set key pair.
    pvk, pbk = crypto.get_key_pair_from_pvk_pem_file(args.pem_path, crypto.KeyEncoding.HEX)

    # Set faucet.
    network.faucet = factory.create_account(
        network=network.name,
        typeof=AccountType.FAUCET,
        index=0,
        private_key=pvk,
        public_key=pbk,
    )

    # Push.
    cache.infra.set_network(network)

    # Inform.
    logger.log(f"Network {args.network} faucet key was successfully registered")


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
