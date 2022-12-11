# Prefect Test: Deployment Test
testing a potential bug in local filesystem storage upload

* Prefect 2.7.1
* Python 3.11
* Environment managed by poetry but not necessary for this test

## SUMMARY
Deployment to block storage subdirectory using `--path` does not copy/upload files to the storage block, its just written to the working directory.

## SETUP
```sh
git clone https://github.com/mahiki/prefect_deploy_test.git

export PREFECT_HOME="${HOME}/.prefect_test"

python src/basic_flow.py
# 10:05:05.317 | INFO    | prefect.engine - Created flow run 'wisteria-dogfish' for flow 'my-favorite-function'
# What is your favorite number?
# 10:05:05.415 | INFO    | Flow run 'wisteria-dogfish' - Finished in state Completed()
# 42

prefect block register --file src/blocks/fs_storage.py
prefect block inspect local-file-system/local-storage
#                              local-file-system/local-storage
# ┌─────────────────┬─────────────────────────────────────────────────────────────────────┐
# │ Block Type      │ Local File System                                                   │
# │ Block id        │ 55a58c9e-72a3-4cfc-8327-4d4e07c5bfd1                                │
# ├─────────────────┼─────────────────────────────────────────────────────────────────────┤
# │ basepath        │ /Users/mithral/.prefect_test/prefect-test-storage                   │
# └─────────────────┴─────────────────────────────────────────────────────────────────────┘
```

## BUG: DEPLOYMENT WITH `--path` IS UPLOADING FILES TO WRONG DIRECTORY
The `--path` option is not behaving as expected, source files being uploaded/copied to working directory. I have not tested s3 storage. Same behavior is observed for `--path` build argument, or using the `--storage-block 'local-file-system/local-storage/subdir'` option.

>An optional path to specify a subdirectory of remote storage to upload to, or to point to a subdirectory of a locally stored flow.

Expected behavior is that the deployed source code is copied to the local-file-system block location, under a subdirectory named `deploy_test`. Instead this happens:

```sh
prefect deployment build \
    src/basic_flow.py:basic_favorite \
    --name "TEST DEPLOYMENT STORAGE" \
    --work-queue test \
    --storage-block 'local-file-system/local-storage' \
    --path 'deploy_test'

# Found flow 'basic-favorite'
# Deployment YAML created at '/Users/mithral/repo/prefect/prefect_deploy_test/basic_favorite-deployment.yaml'.

tree -L 4
.
├── deploy_test         # <--- this is where it gets weird
│   ├── deploy_test
│   │   ├── src
│   │   │   ├── blocks
│   │   │   ├── __init__.py
│   │   │   └── basic_flow.py
│   │   ├── README.md
│   │   ├── basic_favorite-deployment.yaml
│   │   ├── poetry.lock
│   │   └── pyproject.toml
│   ├── src
│   │   ├── blocks
│   │   │   └── fs_storage.py
│   │   ├── __init__.py
│   │   └── basic_flow.py
│   ├── README.md
│   ├── basic_favorite-deployment.yaml
│   ├── poetry.lock
│   └── pyproject.toml
├── src
│   ├── blocks
│   │   └── fs_storage.py
│   ├── __init__.py
│   └── basic_flow.py
├── .env
├── .prefectignore
├── README.md
├── basic_favorite-deployment.yaml
├── poetry.lock
└── pyproject.toml
```

## NORMAL: DEPLOYMENT WITHOUT `--path` IS NORMAL
Expected behavior is getting flow code copied to a local file system location, in this case defined as `$PREFECT_HOME/prefect-test-storage`.

```sh
prefect deployment build \
    src/basic_flow.py:basic_favorite \
    --name "TEST DEPLOYMENT STORAGE" \
    --work-queue test \
    --storage-block 'local-file-system/local-storage'

tree $PREFECT_HOME/prefect-test-storage
/Users/mithral/.prefect_test/prefect-test-storage
├── src
│   ├── blocks
│   ├── __init__.py
│   └── basic_flow.py
├── README.md
├── basic_favorite-deployment.yaml
├── poetry.lock
└── pyproject.toml
```
