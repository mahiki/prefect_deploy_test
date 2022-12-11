# Prefect Test: Deployment Test
testing a potential bug in local filesystem storage upload

* Prefect 2.7.1
* Python 3.11
* Environment managed by poetry but not necessary for this test

## SETUP
```sh
git clone https://github.com/mahiki/prefect_deploy_test.git

export PREFECT_HOME="${HOME}/.prefect_test"

python src/basic_flow.py
# 10:05:05.317 | INFO    | prefect.engine - Created flow run 'wisteria-dogfish' for flow 'my-favorite-function'
# What is your favorite number?
# 10:05:05.415 | INFO    | Flow run 'wisteria-dogfish' - Finished in state Completed()
# 42

# other terminal
prefect orion start


```