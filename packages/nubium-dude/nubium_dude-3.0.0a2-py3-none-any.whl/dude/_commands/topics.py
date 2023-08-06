import importlib
import json

import click
from nubium_schemas.nubium_shared_apps.eloqua import eloqua_retriever_timestamp

from . import dude_cli
from .cli_base import _init_kafka_toolbox, _pass_kafka_toolbox


def _must_be_a_valid_nubium_schema_import(ctx, param, value):
    if value is not None:
        try:
            components = value.split(".")
            module = importlib.import_module(".".join(["nubium_schemas"] + components[0:-1]))
            return getattr(module, components[-1])
        except ImportError as exc:
            raise click.BadParameter(
                ctx=ctx, param=param, message=f'"{value}" is not a valid python attribute to import'
            ) from exc
    return value


def _require_schema_file_when_schema_not_prestent(ctx, param, value):
    if value is None and ctx.params["schema"] is None:
        raise click.MissingParameter(ctx=ctx, param=param, message="Required if --schema not present")
    return value


def _get_cluster_for_topic(kafka_toolbox, topic):
    topics = kafka_toolbox.list_topics(by_topic=True)
    return topics[topic]


@dude_cli.group("topics")
@click.pass_context
def topics_group(ctx):
    ctx.obj = _init_kafka_toolbox(ctx)


@_pass_kafka_toolbox
def create_all_topics(kafka_toolbox, ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    kafka_toolbox.create_all_topics()
    ctx.exit()


@topics_group.command(name="create")
@_pass_kafka_toolbox
@click.option("--all", is_flag=True, expose_value=False, is_eager=True, callback=create_all_topics)
@click.option("--topics", type=str, required=True)
@click.option("--num-partitions", type=int, default=3)
@click.option("--replication-factor", type=int, default=3)
@click.option("--topic-config", type=dict, default={})
def create_topics(kafka_toolbox, topics, num_partitions, replication_factor, topic_config):
    cluster = next(iter(kafka_toolbox.admin_clients))
    kafka_toolbox.create_topics(
        {topic: cluster for topic in topics.split(",")},
        num_partitions=num_partitions,
        replication_factor=replication_factor,
        topic_config=topic_config,
    )


@topics_group.command(name="delete")
@_pass_kafka_toolbox
@click.option("--topics", type=str, required=True)
def delete_topics(kafka_toolbox, topics):
    for topic in topics.split(","):
        cluster = _get_cluster_for_topic(kafka_toolbox, topic)
        kafka_toolbox.delete_topics(
            {topic: cluster for topic in topics.split(",")},
        )


@topics_group.command(name="list")
@_pass_kafka_toolbox
@click.option("--by-topic", type=bool, default=False)
@click.option("--mirrors", type=bool, default=False)
def list_topics(kafka_toolbox, by_topic, mirrors):
    click.echo(
        json.dumps(
            kafka_toolbox.list_topics(
                by_topic=by_topic,
                mirrors=mirrors,
            ),
            indent=4,
        )
    )


@topics_group.command(name="produce")
@_pass_kafka_toolbox
@click.option("--topic", required=True)
@click.option("--message-file", required=True, type=click.File("r"))
@click.option(
    "--schema",
    callback=_must_be_a_valid_nubium_schema_import,
    help="Path to import schema from nubium_schemas Ex: people_stream.person_schema",
)
def produce_message(kafka_toolbox, topic, message_file, schema):
    messages = json.loads(message_file.read())
    kafka_toolbox.produce_messages(
        topic=topic,
        message_list=messages,
        schema=schema,
    )


def format_message(message):
    return {
        "headers": {key: value.decode("utf-8") for key, value in dict(message.headers()).items()},
        "key": message.key(),
        "value": message.value(),
        "timestamp": message.timestamp(),
    }


@topics_group.command(name="consume")
@_pass_kafka_toolbox
@click.option("--topic", required=True)
@click.option("--message-file", required=True, type=click.File("w"))
def consume_message(kafka_toolbox, topic, message_file):
    messages = kafka_toolbox.consume_messages(
        topics=topic,
    )
    json.dump(
        [format_message(message) for message in messages] if messages else [], message_file, indent=4, sort_keys=True
    )


@topics_group.command(name="timestamp")
@_pass_kafka_toolbox
@click.option("--topic", required=True)
@click.option("--time", required=True)
def produce_timestamp(kafka_toolbox, topic, time):
    kafka_toolbox.produce_messages(
        topic=topic,
        schema=eloqua_retriever_timestamp,
        message_list=[
            dict(headers={"guid": "N/A", "last_updated_by": "dude"}, key="dude_timestamp", value={"timestamp": time})
        ],
    )
