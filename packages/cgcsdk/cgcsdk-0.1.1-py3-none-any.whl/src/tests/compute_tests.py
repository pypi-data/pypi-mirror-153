import ast, time
from click.testing import CliRunner

# pylint: disable=import-error
from commands.compute.compute_cmd import compute_group

NAME = "test-pod"


def test_compute_list(volume="none"):
    runner = CliRunner()
    result = runner.invoke(compute_group, ["--debug", "list"])
    timeout = 0
    data = ast.literal_eval(result.output.strip())

    if volume != "none":
        while len(data) == 3 and timeout < 20:
            print(". ", end="", flush=True)
            time.sleep(3)
            timeout += 1
            result = runner.invoke(compute_group, ["--debug", "list"])
            data = ast.literal_eval(result.output.strip())
        print()

        assert (
            len(data) == 2
            and data[0][1] == "filebrowser"
            and data[0][3] == volume
            and data[1][0] == NAME
            and data[1][3] == volume
            and data[1][9] != "none"
        ), f"COMPUTE LIST TEST FAILED: volume{volume}"
    else:
        while len(data) != 1 and timeout < 20:
            print(". ", end="", flush=True)
            time.sleep(3)
            timeout += 1
            result = runner.invoke(compute_group, ["--debug", "list"])
            try:
                data = ast.literal_eval(result.output.strip())
            except SyntaxError:
                print("COMPUTE LIST TEST FAILED: SyntaxError")
                return
        print()
        assert (
            len(data) == 1 and data[0][1] == "filebrowser" and data[0][3] == volume
        ), f"COMPUTE LIST TEST FAILED: volume{volume}"

    print("COMPUTE LIST TEST OK")


def test_compute_create(volume):
    runner = CliRunner()
    result = runner.invoke(
        compute_group,
        ["create", "tensorflow-jupyter", "--name", NAME, "--volume", "test-volume"],
    )
    assert (
        f"OK! tensorflow-jupyter Pod {NAME} has been successfully created! Mounted volumes: ['{volume}']"
        in result.output
    ), "COMPUTE CREATE TEST FAILED"
    print("COMPUTE CREATE TEST OK")


def test_compute_delete():
    runner = CliRunner()
    result = runner.invoke(
        compute_group,
        ["delete", "--name", NAME],
    )
    assert (
        result.output.strip() == f"OK! Pod {NAME} successfully deleted"
    ), "COMPUTE DELETE TEST FAILED"
    print("COMPUTE DELETE TEST OK")
