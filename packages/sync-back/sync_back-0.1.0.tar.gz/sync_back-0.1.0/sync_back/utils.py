from collections.abc import Iterator
from dataclasses import dataclass, field
import logging
import os
from pathlib import Path
import random
import subprocess
import sys
from time import perf_counter
from typing import List, Iterator


from sync_back.progress_bar import job_progress


@dataclass
class FileObject:
    name: Path
    hash: str
    size: int


@dataclass
class StorageSlice:
    files: List[FileObject]
    size: int = 0
    _rsync_path: str = ""

    def get_used(self) -> int:
        self.size = sum([x.size for x in self.files])
        return self.size

    def get_parent(self) -> str:
        shortest_path = min([str(x.name) for x in self.files], key=len)
        self._rsync_path = Path(shortest_path).parent.absolute()
        return self._rsync_path


@dataclass
class StorageDisk:
    path: str
    capacity: int
    size: int = 0
    slices: List[StorageSlice] = field(default_factory=list)

    def get_used(self) -> int:
        self.size = sum([x.size for x in self.slices])
        return self.size


def timer_dec(func):
    def wrap_func(*args, **kwargs):
        t1 = perf_counter()
        result = func(*args, **kwargs)
        t2 = perf_counter()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.8f}s")
        return result

    return wrap_func


def _walk(directory: str) -> Iterator[Path]:
    path = Path(directory)
    for p in path.rglob("*"):
        if p.is_file() and ".bsync" not in p.name and ".DS_Store" not in p.name:
            yield p
        else:
            continue


def walk(directory: str) -> Iterator[FileObject]:
    for file in _walk(directory):
        # print(f"{hash(file).to_bytes(8,'big',signed=True).hex()} - {file}")
        yield FileObject(
            name=file,
            hash=hash(file).to_bytes(8, "big", signed=True).hex(),
            size=file.stat().st_size,
        )


# @timer_dec
def _compute_size_1(all_files: List[FileObject]) -> int:
    count = 0
    for file in all_files:
        count += file.size
    return count


# @timer_dec
def _compute_size_2(all_files: List[FileObject]) -> int:
    return sum([x.size for x in all_files])


def compute_files_size(all_files: List[FileObject]):
    """
    According to the tests, just running sum is faster.

    long_list = [obj for obj in walk(
        "/Users/adaigle/Documents/bancroft/sync_back/test_folders/source")
    ]
    print(_compute_size_1(long_list))
    print(_compute_size_2(long_list))
    """
    return _compute_size_2(all_files=all_files)


def compute_disk_size(path: Path) -> int:
    disk = os.statvfs(path)
    return disk.f_bavail * disk.f_frsize


def group_folders_together(
    all_files: List[FileObject], slice: int
) -> List[StorageSlice]:
    """
    Group files/folders together based on a minimum size.

    This is not optimized because:
    - I don't want something difficult to reason about when things go wrong
        (which they will and already have.)
    - I can't be bothered to think too much about a better algorithm right now.
        It's sunday night and I just want to backup to my drives, get a PoC.

    [
      StorageSlice(
          size=1423413,
          files=[ FileObject(...), ... ],
      )
    ]
    """
    out = []

    # Put the first one in.
    last_file = all_files[0]
    out.append(StorageSlice(files=[last_file]))
    for file in all_files[1:]:

        last_slice = out[-1]
        if file.name.parent != last_file.name.parent and last_slice.get_used() > slice:
            out.append(StorageSlice(files=[file]))
            last_file = file

        else:
            last_slice.files.append(file)
            last_file = file

    return out


def assign_slice_to_disk(
    all_slices: List[StorageSlice], all_disks: List[StorageDisk]
) -> List[StorageDisk]:
    """

    [
      StorageDisk(
          path=PosixPath(...),
          capacity=98989898,
          size=0 <- important
          slices=[ StorageSlice(...), ...],
      )
    ]
    """

    one_percent = [x.capacity * 0.01 for x in all_disks]
    one_percent_cap = sum(one_percent)

    space_needed = sum([slice.get_used() for slice in all_slices])
    percent_needed = space_needed / one_percent_cap

    if any([space_needed < x for x in one_percent]):
        logging.warning(
            "\nYou're trying to store less than 1% of any drives total capacity. "
            "This will place all data on a single drive. Are you sure this is "
            "what you want?"
        )
        selection = input("Continue with this operation? [y/N]\n> ")
        if "y" not in selection.lower():
            sys.exit("User selected to abort backup command.")

    last_slice = all_slices[0]
    disk_counter = 0
    all_disks[disk_counter].slices = [last_slice]
    for slice in all_slices[1:]:

        last_disk = all_disks[disk_counter]
        if last_disk.get_used() / last_disk.capacity > percent_needed:
            disk_counter += 1
            all_disks[disk_counter].slices = [slice]
        else:
            last_disk.slices.append(slice)

        last_slice = slice

    return all_disks


def enforce_path(path) -> str:
    if str(path)[-1] != "/":
        return f"{path}/"
    return str(path)


def rsync_data(
    source_path: Path,
    destination_path: Path,
):
    """
    do a thing...
    """
    # so if the destination folder doesn't exist  then that's problematic... ARG!
    subprocess.check_output(["mkdir", "-p", f"{destination_path.parent}"])

    source_path = enforce_path(source_path)
    destination_path = enforce_path(destination_path)

    job_progress.console.log(f"Copying: {source_path}")
    return subprocess.check_output(
        [
            "rsync",
            "--archive",
            "--human-readable",
            "--verbose",
            "--partial",
            "--progress",
            # "--mkpath",
            # "--copy-dirlinks",
            "--perms",
            "--open-noatime",
            # "--preallocate",
            str(source_path),
            str(destination_path),
        ]
    )


def move_data_around(disk, src, idx):
    for slice in disk.slices:
        destination = Path(str(slice.get_parent()).replace(str(src), str(disk.path)))
        rsync_data(source_path=slice.get_parent(), destination_path=destination)
        job_progress.advance(idx)


if __name__ == "__main__":
    for obj in walk(Path(__file__).parent.parent / "test_folders/forward/source"):
        print(obj)
