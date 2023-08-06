import click

from . import dude_cli
from .cli_base import _init_kafka_toolbox, _pass_kafka_toolbox


@dude_cli.group("app")
@click.pass_context
def app_group(ctx):
    ctx.obj = _init_kafka_toolbox(ctx)


@app_group.command("run")
@_pass_kafka_toolbox
@click.option("--skip-topic-creation", is_flag=True)
@click.option("--skip-sync", is_flag=True)
@click.argument("run-args", nargs=-1, type=str)
def run(kafka_toolbox, skip_topic_creation, skip_sync, run_args):
    kafka_toolbox.run_app(skip_topic_creation, skip_sync, run_args)


@app_group.command("sync")
@_pass_kafka_toolbox
@click.option("--wipe-existing", is_flag=True)
def sync(kafka_toolbox, wipe_existing):
    kafka_toolbox.sync_venv(wipe_existing)


@click.argument("extra_pytest_args", nargs=-1, type=click.UNPROCESSED)
@app_group.command("unit_test", context_settings={"ignore_unknown_options": True})
@_pass_kafka_toolbox
def unit_test(kafka_toolbox, extra_pytest_args):
    kafka_toolbox.run_unit_tests(extra_pytest_args=list(extra_pytest_args))


@click.argument("extra_pytest_args", nargs=-1, type=click.UNPROCESSED)
@app_group.command("integration_test", context_settings={"ignore_unknown_options": True})
@_pass_kafka_toolbox
def integration_test(kafka_toolbox, extra_pytest_args):
    kafka_toolbox.run_integration_tests(extra_pytest_args=list(extra_pytest_args))


@app_group.command("build_reqs")
@_pass_kafka_toolbox
def build_requirements(kafka_toolbox):
    kafka_toolbox.build_reqs()
