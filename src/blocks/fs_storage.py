from pathlib import Path
from prefect.filesystems import LocalFileSystem

fs_block = LocalFileSystem(
    basepath=Path.home().joinpath(".prefect_test","prefect_test_storage")
    )
fs_block.save(name="local_storage_block", overwrite=True)
