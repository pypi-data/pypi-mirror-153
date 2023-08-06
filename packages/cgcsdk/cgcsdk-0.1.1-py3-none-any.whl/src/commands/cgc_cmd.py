import click

# pylint: disable=import-error
from commands.compute.compute_cmd import compute_delete


@click.command("rm")
@click.option("-n", "--name", "name", type=click.STRING, required=True)
def cgc_rm(name: str):
    """
    Wrapper for compute_delete as command cgc rm

    :param name: name of pod to delete
    :type name: str
    """
    compute_delete(name)
