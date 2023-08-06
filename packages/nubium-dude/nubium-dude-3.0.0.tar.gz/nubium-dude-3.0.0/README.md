View documentation @ [https://mkt-ops-de.pages.corp.redhat.com/dude](https://mkt-ops-de.pages.corp.redhat.com/dude) or
build it locally via `tox -e docs`

# Installation and Setup

```
pipx install --python python3.8 nubium-dude
```

## Configuration

As most CLI tools do, dude loads configuration in a hiearchial order:
1. defaults
2. config file
3. environment variables
4. command line options
5. environment variables that are sourced from `dotenv_files` key in the configuration
6. environment variables that are sourced from `./venv/local.env`

`tests/test_config.py` has examples of configuration files, here's one of them:
```
environments:
  default:
    clusters:
      default-A:
        bootstrap_urls: ["localhost", "kafka-1"]
  override:
    clusters:
      override-A:
        bootstrap_urls: ["localhost", "kafka-1"]
default_environment: default
```
The config file can be edited with `dude config edit`. This will launch a text
editor configured by either of the `VISUAL` or `EDITOR` environment variables.
The default path can be configured by setting `DUDE_CONFIG_FILE` with the full
path to an alternative yaml file.
If `DUDE_CONFIG_FILE` is not specified, an example default location 
(on Mac OS) is "/Users/[username]/Library/Application Support/dude/config.yaml".


### Special tags
Any value can be dynamically computed frome these tags

#### !Environment
key's value would be `os.environ["VAR_NAME"]`
```
key: !Environment VAR_NAME
```

#### !DotEnv
key's value would be `dotenv_values("PATH")["VAR"]`
```
key: !DotEnv [PATH, VAR]
```
For more information on the dotenv syntax for the file pointed to by PATH, refer to see (dotenv's documentation)[https://github.com/theskumar/python-dotenv#file-format]

### Remnants of the previous configuration
```
HOSTNAME=""
RHOSAK_USERNAME=(nubium-secrets.rhosakUsername)
RHOSAK_PASSWORD=(nubium-secrets.rhosakPassword)
SCHEMA_REGISTRY_USERNAME=(nubium-secrets.rhosakUsername)
SCHEMA_REGISTRY_PASSWORD=(nubium-secrets.rhosakPassword)
SCHEMA_REGISTRY_URL=(nubium-secrets.schemaRegistryUrl)
```
Example Openshift Secret: https://manage.preprod.iad2.dc.paas.redhat.com/console/project/mktg-ops--nubium-dev/browse/secrets/nubium-secrets

# Usage

`dude --help` or `dude subcommand --help`

## Managing Topics

### List topics

`dude topics list`

Topics will be listed by cluster.

### Create topics

`dude topics create --topics topic_a,topic_b`

If a topic is defined in the selected environment's configuration, then it will be created with the same configuration
defined in that file. Otherwise, the topic is created with a default configuration (note: `dude topics create --help`
will show the defaults).

### Create topics with custom partitions and replication factor

`dude topics create --topics topic_a --num-partitions 2 --replication-factor 2`

### Create topics on your `TEST_CLUSTER`, ignoring cluster maps in `cluster.py`

`dude topics create --topics topic_a,topic_b --ignore-cluster-maps`

### Delete topics

`dude topics delete --topics topic_a,topic_b`

If the topic exists in `nubium_schemas/nubium_topic_configs/clusters.py`, `dude` will try to delete the topic from the
assigned cluster.  Passing `--ignore-cluster-maps` will instruct `dude` to delete the topic from your `TEST_CLUSTER`.

## Producing and Consuming

### Produce to a topic from a json file

`dude topics produce --topic topic_a --message-file test_data_in.json --schema nubium_integrations.dynamic_form.eloqua_form`

The parameter `--schema` must be a valid path to import the schema from `nubium_schemas`.

### Consume all messages from a topic and dump to a json file

`dude topics consume --topic topic_a --message-file test_data_out.json`

NOTE: in the future, we would like to add an option to the `dude topics consume` function so that you may choose to
consume from your consumer group's latest offset instead of consuming everything.

## App

### Build requirements.txt

(in app root folder): `dude app build_reqs`

### Run app

(in app root folder): `dude app run`

### Run unit tests

(in app root folder): `dude app unit_test`

### Run integration test

(in app root folder): `dude app integration_test`

# Contributing
Run tests via:
```
pipx install tox
pipx inject tox tox-pyenv
tox
```

Pass extra arguments to pytest:
```
# run tests that have "translates" in their name
tox -e py38 -- -k translates
```

## Pipx isolated environments
If you want to run the `dude` script based on changes in your local repo, use
the editable option when installing with pipx:
```
pipx install -e /PATH/TO/DUDE/REPO
```

You can also inject editable versions of dependencies like this:
```
pipx inject nubium-dude -e /PATH/TO/nubium-schemas
pipx inject nubium-dude -e /PATH/TO/nubium-utils
```
(Useful command for confirming whether you are using local repos for requirements: `pipx runpip nubium-dude freeze`)
