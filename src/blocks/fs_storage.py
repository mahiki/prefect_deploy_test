from pathlib import Path
from prefect.filesystems import LocalFileSystem

fs_block = LocalFileSystem(
    basepath=Path.home().joinpath(".prefect_test","prefect-test-storage")
    )
fs_block.save(name="local-storage", overwrite=True)
