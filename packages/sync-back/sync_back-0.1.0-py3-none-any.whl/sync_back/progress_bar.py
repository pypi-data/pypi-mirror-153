from rich.progress import (
    Progress,
    # SpinnerColumn,
    BarColumn,
    TextColumn,
    # FileSizeColumn,
    # TransferSpeedColumn,
    # TimeElapsedColumn,
    # DownloadColumn,
    TimeRemainingColumn,
)

job_progress = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TextColumn("eta"),
    TimeRemainingColumn(),
)
