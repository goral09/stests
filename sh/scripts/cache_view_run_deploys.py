import argparse
import statistics

from beautifultable import BeautifulTable

from stests.core import cache
from stests.core import factory
from stests.core.types.chain import DeployStatus
from stests.core.types.orchestration import ExecutionAspect
from stests.core.utils import args_validator
from stests.core.utils import cli as utils



# CLI argument parser.
ARGS = argparse.ArgumentParser("Displays summary information for a run.")

# CLI argument: network name.
ARGS.add_argument(
    "--net",
    default="nctl1",
    dest="network",
    help="Network name {type}{id}, e.g. nctl1.",
    type=args_validator.validate_network,
    )

# CLI argument: run type.
ARGS.add_argument(
    "--run-type",
    dest="run_type",
    help="Generator type - e.g. wg-100.",
    type=args_validator.validate_run_type,
    )

# CLI argument: run index.
ARGS.add_argument(
    "--run",
    dest="run_index",
    help="Run identifier.",
    type=args_validator.validate_run_index,
    )


# Table columns.
COLS = [
    ("#", BeautifulTable.ALIGN_LEFT),
    ("Dispatch Timestamp", BeautifulTable.ALIGN_LEFT),
    ("Dispatch Node", BeautifulTable.ALIGN_LEFT),
    ("Deploy Hash", BeautifulTable.ALIGN_LEFT),
    ("Type", BeautifulTable.ALIGN_LEFT),
    ("Status", BeautifulTable.ALIGN_LEFT),
    ("Dispatch Account", BeautifulTable.ALIGN_LEFT),
    ("Finalization Time", BeautifulTable.ALIGN_RIGHT),
    ("Round ID", BeautifulTable.ALIGN_RIGHT),
    ("Block Hash", BeautifulTable.ALIGN_RIGHT),
]


def main(args):
    """Entry point.
    
    :param args: Parsed CLI arguments.

    """
    # Pull data.
    network_id = factory.create_network_id(args.network)
    data = cache.state.get_deploys(network_id, args.run_type, args.run_index)
    if not data:
        utils.log("No run deploys found.")
        return

    # Render views.
    _render_table(args, network_id, data)
    _render_finalization_stats(data)


def _render_table(args, network_id, data):
    # Sort data.
    data = sorted(data, key=lambda i: i.dispatch_timestamp)

    # Set table cols/rows.
    cols = [i for i, _ in COLS]
    rows = map(lambda i: [
        data.index(i) + 1,
        i.dispatch_timestamp,
        i.dispatch_node,
        i.deploy_hash,      
        i.typeof.name,
        i.status.name,      
        i.account,
        i.label_finalization_duration,
        i.round_id or "--",
        i.block_hash or "--"
    ], data)

    # Set table.
    t = utils.get_table(cols, rows)

    # Set table alignments.
    for key, aligmnent in COLS:
        t.column_alignments[key] = aligmnent    

    # Render.
    print(t)
    print(f"{network_id.name} - {args.run_type}  - Run {args.run_index}")


def _render_finalization_stats(data):
    """Renders finalization stats.
    
    """
    times = [i.finalization_duration for i in data if i.finalization_duration]
    if not times:
        return

    maxima = max(times)
    minima = min(times)
    avg = statistics.mean(times)
    stdev = statistics.stdev(times)
    # variance = format(statistics.variance(times), '.3f') if len(times) > 1 else 'N/A'

    # print(f"Finalized = {len(times)} :: %={int((len(times) / len(data)) * 100)} :: Avg={format(avg, '.3f')}s :: Max={format(maxima, '.3f')}s :: Min={format(minima, '.3f')}s :: Variance={variance}s :: Std Dev= {format(stdev, '.3f')}s")
    print(f"Finalized = {len(times)} :: %={int((len(times) / len(data)) * 100)} :: Avg={format(avg, '.3f')}s :: Max={format(maxima, '.3f')}s :: Min={format(minima, '.3f')}s :: Std Dev= {format(stdev, '.3f')}s")

# Entry point.
if __name__ == '__main__':
    main(ARGS.parse_args())
