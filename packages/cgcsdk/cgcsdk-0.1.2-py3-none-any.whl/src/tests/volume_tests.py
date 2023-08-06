import json, ast
from click.testing import CliRunner


# pylint: disable=import-error
from commands.volume.volume_cmd import volume_group


def test_volume_list(volume=""):
    runner = CliRunner()
    result = runner.invoke(volume_group, ["--debug", "list"])

    if volume == "":
        assert (
            result.output.strip() == "No volumes to list."
        ), "VOLUME LIST TEST FAILED1"
    else:
        data = ast.literal_eval(result.output.strip())
        assert (
            len(data) == 1 and volume in data[0] and "1Gi" in data[0]
        ), "VOLUME LIST TEST FAILED2"
    print("VOLUME LIST TEST OK")


def test_volume_create(volume):
    runner = CliRunner()
    result = runner.invoke(volume_group, ["create", volume, "--size", 1])
    assert (
        result.output.strip()
        == f"OK! Volume {volume} of size 1Gi GB on SSD created from imported module. Volume is ReadWriteMany."
    ), "VOLUME CREATE TEST FAILED"
    print("VOLUME CREATE TEST OK")


def test_volume_delete(volume):
    runner = CliRunner()
    result = runner.invoke(volume_group, ["delete", volume, "--force"])
    assert (
        result.output.strip() == "OK! Volume test-volume deleted."
    ), "VOLUME DELETE TEST FAILED"
    print("VOLUME DELETE TEST OK")
