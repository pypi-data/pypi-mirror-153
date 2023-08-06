import click, requests, json
from tabulate import tabulate

# pylint: disable=import-error
from commands.compute.compute_responses import compute_create_response
from commands.compute.compute_responses import compute_delete_response
from commands.compute.data_model import compute_create_payload_validator
from commands.compute.data_model import compute_delete_payload_validator
from commands.compute.compute_utills import list_get_pod_list_to_print
from utils.prepare_headers import get_api_url_and_prepare_headers
from telemetry.basic import incrementMetric
from telemetry.basic import setupGauge

API_URL, headers = get_api_url_and_prepare_headers()


@click.group("compute")
@click.option("--debug", "debug", is_flag=True, default=False, hidden=True)
@click.pass_context
def compute_group(ctx, debug):
    """
    Group to store all the compute commands.
    """
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug


@compute_group.command("create")
@click.argument("entity", type=click.Choice(["tensorflow-jupyter"]))
@click.option("-n", "--name", "name", type=click.STRING, required=True)
@click.option("-g", "--gpu", "gpu", type=click.IntRange(0, 8), default=0)
# TODO ustalic z backendem jakie parametry podajemy. I jaki wysyłamy jako default czyli maszyna bez GPU
@click.option(
    "-gt", "--gpu-type", "gpu_type", type=click.Choice(["A100", "V100", "A5000"])
)
@click.option("-c", "--cpu", "cpu", type=click.INT, default=1)
@click.option("-m", "--memory", "memory", type=click.INT, default=2)
@click.option("-v", "--volume", "volumes", multiple=True)
def compute_create(
    entity: str,
    gpu: int,
    gpu_type: str,
    cpu: int,
    memory: int,
    volumes: list[str],
    name: str,
):
    """
    Create a compute pod using backend endpoint

    :param entity: name of entity to create
    :type entity: str
    :param gpu: number of gpus to be used by pod
    :type gpu: int
    :param cpu: number of cores to be used by pod
    :type cpu: int
    :param memory: GB of memory to be used by pod
    :type memory: int
    :param volumes: list of volumes to mount
    :type volumes: list[str]
    :param name: name of pod
    :type name: str
    """

    url = f"{API_URL}/v1/api/compute/create"

    payload = compute_create_payload_validator(
        name=name,
        entity=entity,
        cpu=cpu,
        memory=memory,
        gpu=gpu,
        volumes=volumes,
        gpu_type=gpu_type,
    )
    try:
        res = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(compute_create_response(res))
    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


@compute_group.command("delete")
@click.option("-n", "--name", "name", type=click.STRING, required=True)
def compute_delete_cmd(name: str):
    """
    Wrapper for compute_delete as command cgc compute delete

    :param name: name of pod to delete
    :type name: str
    """
    compute_delete(name)


def compute_delete(name: str):
    """
    Delete a compute pod using backend endpoint

    :param name: name of pod to delete
    :type name: str
    """
    url = f"{API_URL}/v1/api/compute/delete"
    payload = compute_delete_payload_validator(name=name)
    try:
        res = requests.delete(
            url,
            data=json.dumps(payload),
            headers=headers,
            timeout=10,
        )
        click.echo(compute_delete_response(res))
    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )


@compute_group.command("list")
@click.pass_context
def compute_list(ctx):
    """
    List all pods for user namespace
    """

    url = f"{API_URL}/v1/api/compute/list"
    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            namespace = data["details"]["namespace"]
            pod_list = data["details"]["pods_list"]

            setupGauge(f"{namespace}.compute.count", len(pod_list))
            incrementMetric(f"{namespace}.compute.list.ok")

            if not pod_list:
                click.echo("No pods to list.")
                return

            pod_list_to_print = list_get_pod_list_to_print(pod_list)

            list_headers = [
                "name",
                "type",
                "status",
                "volumes mounted",
                "CPU cores",
                "RAM",
                "GPU type",
                "GPU count",
                "URL",
                "Jupyter token",
            ]

            if ctx.obj["DEBUG"]:
                print(pod_list_to_print)
            else:
                click.echo(tabulate(pod_list_to_print, headers=list_headers))
        else:
            # TODO jakie errory może zwracać backend? Czy jest tam zaszyty namespace?
            incrementMetric("compute.list.error")
            click.echo(f"Error: {response.status_code} {response.text}")
    except requests.exceptions.ReadTimeout:
        click.echo(
            "Connection timed out. Try again or contact us at support@comtegra.pl"
        )
