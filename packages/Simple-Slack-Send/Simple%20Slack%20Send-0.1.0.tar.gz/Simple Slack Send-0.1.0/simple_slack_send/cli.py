import os
import click
import re

import requests

from simple_slack_send.loader import VarsLoader, json_file_to_dict


def check_var(ctx, param, value):
    for v in value:
        if not re.match("^[^=]+=.*$", v):
            raise click.BadParameter(
                f"'{v}'. Variable has to be in format variable=value"
            )
    return value


# fmt: off
@click.command()
@click.argument("msg-file", type=str)
@click.option("--env-file", "-e", multiple=True, type=str, help="Path to env-style file with variables")
@click.option("--json-file", "-j", multiple=True, type=str, help="Path to json file with variable")
@click.option("--var", "-v", multiple=True, type=str, callback=check_var, help="Single variable in format name=value")
@click.option("--sys-env/--no-sys-env", is_flag=True, default=True, help="Uses system env as a source for template variables")
@click.option("--webhook-url", default=None, help="Slack webhook url. If not specified env variable SLACK_WEBHOOK_URL will be used.")
# fmt: on
def send(
    msg_file,
    env_file,
    json_file,
    var,
    sys_env,
    webhook_url,
):
    if webhook_url is None:
        webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    click.echo(f"🚀 Sending slack notification.")
    vars = VarsLoader(env_file, var, json_file, sys_env).load()
    payload = json_file_to_dict(msg_file, vars)
    requests.post(webhook_url, json=payload)
    click.echo(f"\t✅ done.")
