import json
import requests

# pylint: disable=import-error
from telemetry.basic import incrementMetric, changeGauge


def volume_create_error_parser(error: dict) -> str:
    """Function that pases error from API for volume create command.
    For now there is two errors implementned to give string output.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """
    # print(error)
    try:
        if error["reason"] == "AlreadyExists":
            return f"ERROR! Volume with name {error['details']['name']} already exists."
        if error["reason"] == "Invalid":
            #! Sprawdzić bo można sie tu łatwo wywalić
            return error["details"]["causes"][0]["message"]
    except KeyError:
        return "An unecpected error occured. Please try again, change name of the volume or contact support."
    return error


def volume_create_response(response: requests.Response) -> str:
    """Create response string for volume create command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    if response.status_code == 500:
        return "Internal Server Error"

    data = json.loads(response.text)

    def shotTelemetry(size: int, namespace: str):
        """Function that sends telemetry for volume create command.
        Created only because occured error 201. We don't know all the errors yet. 201 creates volume but fires excepion"""
        incrementMetric(f"{namespace}.volume.create.ok")
        changeGauge(f"{namespace}.volume.count", 1)
        changeGauge(f"{namespace}.volume.totalSizeAccumulated", size)

    if response.status_code == 200:
        namespace = data["details"]["namespace"]
        name = data["details"]["volume_created"]["name"]
        size = data["details"]["volume_created"]["size"]
        access = data["details"]["volume_created"]["access_type"][0]
        disk_type = data["details"]["volume_created"]["disks_type"]
        shotTelemetry(int("".join(filter(str.isdigit, size))), namespace)
        return f"OK! Volume {name} of size {size} GB on {disk_type} created from imported module. Volume is {access}."
    if response.status_code == 201:
        error = volume_create_error_parser(data)
        size = data["details"]["volume_created"]["size"]
        shotTelemetry(int("".join(filter(str.isdigit, size))), namespace)
        return error

    else:
        incrementMetric("volume.create.error")
        error = volume_create_error_parser(data)
        return error


def volume_delete_error_parser(error: dict) -> str:
    """Function that pases error from API for volume delete command.
    For now there is one error implementned to give string output.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """

    # print(error)
    try:
        if error["reason"] == "NotFound":
            return f"ERROR! Volume with name {error['details']['name']} not found."
    except KeyError:
        return "An unecpected error occured. Please try again, or contact support at support@comtegra.pl."
    return error


def volume_delete_response(response: requests.Response) -> str:
    """Create response string for volume delete command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    if response.status_code == 500:
        return "Internal Server Error"

    data = json.loads(response.text)

    if response.status_code == 200:
        namespace = data["details"]["namespace"]
        name = data["details"]["volume_deleted"]["name"]
        size = int(
            "".join(filter(str.isdigit, data["details"]["volume_deleted"]["size"]))
        )
        incrementMetric(f"{namespace}.volume.delete.ok")
        changeGauge(f"{namespace}.volume.count", -1)
        changeGauge(f"{namespace}.volume.totalSizeAccumulated", -size)

        return f"OK! Volume {name} deleted."
    incrementMetric("volume.delete.error")
    # TODO other errors if implemented
    error = volume_delete_error_parser(data)
    return error


def volume_response_parser(response: requests.Response, command: str) -> str:
    """Response parser for volume mount and umount.

    :param response: response to parse.
    :type response: requests.Response
    :return: response message string.
    :rtype: str
    """
    try:
        data = json.loads(response.text)
        status = data["status"]
        name = data["details"]["pvc_name"]
        message = data["message"]
        namespace = data["details"]["namespace"]

        if response.status_code == 200:
            incrementMetric(f"{namespace}.volume.{command}.ok")
        else:
            incrementMetric(f"{namespace}.volume.{command}.error")

        return f"{status} for volume {name}: {message}"
    except KeyError:
        incrementMetric(f"volume.{command}.error")
        return f"{data}\nUnknown error occured. Please contact support at support@comtegra.pl"
    except json.JSONDecodeError:
        incrementMetric(f"volume.{command}.error")
        return f"{response.text}\nUnknown error occured. Please contact support at support@comtegra.pl"
