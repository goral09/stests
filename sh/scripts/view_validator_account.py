import argparse
import json

from stests import chain
from stests.core.utils import args_validator
from stests.core.utils import cli as utils
from stests.core.utils import env
from arg_utils import get_network_node
from arg_utils import get_network_nodeset



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays a validators's on-chain account information.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default=env.get_network_name(),
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: node index.
ARGS.add_argument(
    "--node",
    dest="node",
    help="Node index, e.g. 1.",
    type=args_validator.validate_node_index
    )


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    if args.node:
        network, node = get_network_node(args)
        nodeset = [node]
    else:
        network, nodeset = get_network_nodeset(args)

    for node in nodeset:
        utils.log_line()
        utils.log(f"VALIDATOR ACCOUNT @ NODE {node.index} ({node.address}) :")
        account = chain.get_account(network, node, node.account.account_key)
        if account:
            print(json.dumps(account, indent=4))
        else:
            print("Chain query returned null - is the validator account correct ?")

    utils.log_line()


# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
