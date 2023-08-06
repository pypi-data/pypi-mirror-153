import concurrent.futures
import os
from pathlib import Path

import click

from sync_back.utils import (
    assign_slice_to_disk,
    walk,
    compute_files_size,
    compute_disk_size,
    group_folders_together,
    assign_slice_to_disk,
    move_data_around,
    StorageDisk,
)
from sync_back.progress_bar import job_progress


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    """
    Do something with the debug flag... eventually
    """
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@cli.command()
@click.pass_context
def list(ctx):
    if ctx.obj["DEBUG"]:
        click.echo("Debugging...")
    click.echo("List files in a bsync backup")


@cli.command()
@click.pass_context
@click.option(
    "-s",
    "--slice",
    type=int,
    # Grow folder groups to a minimum of 1GB before storage
    # default=1_000_000_000,
    default=1_000_000,
    help=(
        "Smallest size a folder group can take on it's own (as long as there "
        "are enough files of sufficient size to accomidate it."
    ),
)
@click.argument("src", nargs=1)
@click.argument("dst", nargs=-1)
def backup(ctx, slice, src, dst):
    """
    Take a single source directory and copy it to n places.
    """
    # TODO: Do something with debugging at some point... maybe?
    if ctx.obj["DEBUG"]:
        # click.echo(f"Split into: {slice} containers.")
        click.echo(f"Source is: {src}")
        click.echo(f"{Path(src).absolute()}")
        # click.echo(f"Dest.  is: {dst}")

    src = Path(src).absolute()  # Convert user-input source to absolute path
    all_files = [x for x in walk(directory=str(src))]  # [FileObject(...), ...]
    disk_sizes = [compute_disk_size(x) for x in dst]  # [62767923200, ...]

    assert sum(disk_sizes) > compute_files_size(all_files=all_files) * 1.2, (
        "You are trying to store more" "data than there is available space."
    )

    click.echo("Grouping folders together")

    sorted_disks = assign_slice_to_disk(
        all_slices=group_folders_together(all_files=all_files, slice=slice),
        all_disks=[
            StorageDisk(path=path, capacity=size)
            for path, size in zip([Path(p).absolute() for p in dst], disk_sizes)
        ],
    )

    ############################################################################
    # Fancy UI stuff
    ############################################################################

    jobs = {}
    for idx, disk in enumerate(sorted_disks):
        disk.get_used()
        jobs[idx] = job_progress.add_task(
            description=f"{disk.path}",
            total=len(disk.slices),
        )

    with job_progress:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:

            {
                pool.submit(move_data_around, disk, src, idx): idx
                for idx, disk in enumerate(sorted_disks)
            }

    click.echo("Backing up files to disks")


@cli.command()
@click.pass_context
@click.argument("dst", nargs=1)
@click.argument("src", nargs=-1)
def restore(ctx, dst, src):
    click.echo("Restore files from backup")


if __name__ == "__main__":
    cli()
