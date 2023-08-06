import click
import requests
import json

from tabulate import tabulate

# pylint: disable=import-error
from utils.prepare_headers import get_api_url_and_prepare_headers
from telemetry.basic import incrementMetric, setupGauge
from commands.volume.data_model import (
    volume_create_payload_validator,
    volume_delete_payload_validator,
    volume_mount_payload_validator,
    volume_umount_payload_validator,
)
from commands.volume.volume_utils import get_formatted_volume_list_and_total_size
from commands.volume.volume_responses import (
    volume_response_parser,
    volume_create_response,
    volume_delete_response,
)


API_URL, headers = get_api_url_and_prepare_headers()


@click.group("volume")
@click.option("--debug", "debug", is_flag=True, default=False, hidden=True)
@click.pass_context
def volume_group(ctx, debug):
    """
    Group to store all the volume commands.
    """
    # pylint: disable=unnecessary-pass
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@volume_group.command("list")
@click.pass_context
def volume_list(ctx):
    """
    List all volumes for user namespace
    """

    url = f"{API_URL}/v1/api/storage/volume/list"
    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            list_of_volumes = data["details"]["volume_list"]
            namespace = data["details"]["namespace"]

            incrementMetric(f"{namespace}.volume.list.ok")
            setupGauge(f"{namespace}.volume.count", len(list_of_volumes))

            if not list_of_volumes:
                click.echo("No volumes to list.")
                return

            volume_list_to_print, total_size = get_formatted_volume_list_and_total_size(
                list_of_volumes
            )
            list_headers = ["name", "used", "size", "type", "mounted to"]
            setupGauge(f"{namespace}.volume.totalSizeAccumulated", total_size)

            if ctx.obj["DEBUG"]:
                click.echo(volume_list_to_print)
            else:
                click.echo(tabulate(volume_list_to_print, headers=list_headers))

        else:
            # TODO jakie errory może zwracać backend? Czy jest tam zaszyty namespace?
            incrementMetric("volume.list.error")
            click.echo(f"Error: {response.status_code} {response.text}")
    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact support at support@comtegra.pl"
        )


@volume_group.command("create")
# create `<name>*` --size* <int GB> --type <HDD|SSD*> --access <RWO|RWX\*>
@click.argument("name")
# TODO exception on limit excess - backend
@click.option("-s", "--size", "size", type=click.IntRange(1, 1000), required=True)
@click.option(
    "-t", "--type", "disk_type", type=click.Choice(["hdd", "ssd"]), default="ssd"
)
@click.option("-a", "--a", "access", type=click.Choice(["rwx", "rwo"]), default="rwx")
def volume_create(name: str, size: int, disk_type: str, access: str):
    """Main function to create a volume using backend endpoint.

    :param name: _description_
    :type name: str
    :param size: _description_
    :type size: int
    :param type: _description_
    :type type: str
    :param access: _description_
    :type access: str
    """

    url = f"{API_URL}/v1/api/storage/volume/create"
    payload = volume_create_payload_validator(
        name=name,
        access=access,
        size=size,
        disk_type=disk_type,
    )
    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(volume_create_response(res))

    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


@volume_group.command("delete")
# {  "name": "test-volume",  "force_delete": true }
@click.argument("name")
@click.option("-f", "--force", "force_delete", is_flag=True, default=False)
def volume_delete(name: str, force_delete: bool):
    """Delete specific volume from user namespace.

    :param name: name of the volume to delete
    :type name: str
    :param force_delete: delete volume even if it is in use. It umount volume from compute resources.
    :type force_delete: bool
    """
    url = f"{API_URL}/v1/api/storage/volume/delete"
    payload = volume_delete_payload_validator(
        name=name,
        force_delete=force_delete,
    )
    try:
        res = requests.delete(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )

        click.echo(volume_delete_response(res))

    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


@volume_group.command("umount")
# {"name": "test-volume"}
@click.argument("name")
def volume_umount(name: str):
    url = f"{API_URL}/v1/api/storage/volume/umount"
    payload = volume_umount_payload_validator(name=name)

    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(volume_response_parser(res, "umount"))

    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


@volume_group.command("mount")
# {  "name": "test-volume", "target_template_name": "jupyter-notebook", "start_mount_path": "/tf" }
@click.argument("name")
@click.option("-t", "--target", "target", type=str, required=True)
@click.option(
    "-ttt",
    "--target_template_type",
    "target_template_type",
    type=click.Choice(["deployment"]),
)
@click.option("-p", "--mount_path", "mount_path", type=str, default="/tf")
def volume_mount(
    name: str,
    target_template_type: str,
    target: str,
    mount_path: str,
):
    url = f"{API_URL}/v1/api/storage/volume/mount"
    payload = volume_mount_payload_validator(
        name=name,
        target=target,
        target_template_type=target_template_type,
        mount_path=mount_path,
    )
    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )

        click.echo(volume_response_parser(res, "mount"))

    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )
