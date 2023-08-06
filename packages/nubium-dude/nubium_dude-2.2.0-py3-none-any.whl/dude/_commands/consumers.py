import asyncio
from tempfile import NamedTemporaryFile
import subprocess
from dude._utils import as_async
from os import environ
from nubium_utils.confluent_utils import KafkaToolbox
import json
from . import dude_cli
import click


def get_temp_properties_file():
    tmp_file = NamedTemporaryFile(mode='w+', delete=False)
    tmp_file.writelines(f'''\
sasl.mechanism=PLAIN
security.protocol=SASL_SSL
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username = "{environ['RHOSAK_USERNAME']}" password = "{environ['RHOSAK_PASSWORD']}";''')
    tmp_file.flush()
    return tmp_file


def get_cluster_lag(cluster):
    tmp_file = get_temp_properties_file()
    run_str = f"{environ['DUDE_KAFKA_BIN_FOLDER']}/kafka-consumer-groups.sh --bootstrap-server {cluster} --command-config {tmp_file.name} --describe --all-groups --timeout 15000"
    result = ''
    try:
        result = subprocess.run(run_str.split(' '), capture_output=True, text=True, timeout=30)
        if result.stdout:
            return result.stdout
        return ''
    except:
        if hasattr(result, 'stderr'):
            print(result.stderr)
        return ''
    finally:
        tmp_file.close()


def format_cluster_lag(shell_output):
    laglines = [line.split() for line in shell_output.split('\n') if line and not line.startswith('GROUP')]
    laglines = [
        {'group': c[0],
         'topic': c[1],
         'partition': int(c[2]),
         'lag': int(c[5]) - 1 if 'faust' in c[8] else int(c[5]),
         'consumer_id': c[6]}
        for c in laglines if c[5].isnumeric()]
    dict_out = {}
    for line in laglines:
        groups = dict_out.get(line['group'], {})
        topics = groups.get(line['topic'], {})
        cids = topics.get(line['consumer_id'], []) + [{k: line[k] for k in ['partition', 'lag']}]

        topics[line['consumer_id']] = cids
        groups[line['topic']] = topics
        dict_out[line['group']] = groups
    return dict_out


@as_async
def get_cluster_lag_async(cluster):
    return format_cluster_lag(get_cluster_lag(cluster))


async def get_all_cluster_lags_async(kafka_toolbox, counts_only=False):
    final_result = {}
    consumer_lags = await asyncio.gather(*[get_cluster_lag_async(cluster) for cluster in kafka_toolbox.nubium_clusters])
    for lags in consumer_lags:
        for group, topics in lags.items():
            group_data = final_result.get(group, {})
            group_data.update(topics)
            final_result[group] = group_data
    if counts_only:
        count_result = {}
        for group, topics in final_result.items():
            count_result[group] = {**count_result.get(group, {}), **{topic: len(consumers.keys()) for topic, consumers in topics.items()}}
        final_result = count_result
    return final_result


def get_all_cluster_lags(kafka_toolbox, counts=False):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_all_cluster_lags_async(kafka_toolbox, counts))


@dude_cli.group("consumers")
@click.pass_context
@click.option("--bootstrap-servers")
@click.option("--rhosak-username")
@click.option("--rhosak-password")
@click.option("--security-protocol")
@click.option("--sasl-mechanisms")
def consumers_group(ctx, bootstrap_servers, rhosak_username, rhosak_password, security_protocol, sasl_mechanisms):
    ctx.obj = KafkaToolbox(auto_configure=False)


pass_kafka_toolbox = click.make_pass_decorator(KafkaToolbox)


@consumers_group.command(name="list")
@click.option("--group-counts-only", is_flag=True)
@pass_kafka_toolbox
def list_consumer_groups(kafka_toolbox, group_counts_only):
    click.echo(json.dumps(get_all_cluster_lags(kafka_toolbox, group_counts_only), indent=4))
