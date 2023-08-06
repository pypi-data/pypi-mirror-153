import json
import requests


# pylint: disable=import-error
from telemetry.basic import incrementMetric
from telemetry.basic import changeGauge


def compute_create_error_parser(error: dict) -> str:
    """Function that pases error from API for compute create command.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """
    # TODO add errors after backend is finished
    # print(error)
    try:
        if error["reason"] == "AlreadyExists":
            return f"ERROR! Pod with name {error['details']['name']} already exists."
    except KeyError:
        return "An unecpected error occured. Please try again, or contact support at support@comtegra.pl."
    return error


def compute_create_response(response: requests.Response) -> str:
    """Create response string for compute create command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    if response.status_code == 500:
        return "Internal Server Error. Try again or contact us at support@comtegra.pl"

    data = json.loads(response.text)

    if response.status_code == 200:

        namespace = data["details"].get("namespace")
        compute_create_telemetry_shot_ok(namespace=namespace)
        name = data["details"].get("created_service").get("name")
        entity = data["details"].get("created_service").get("labels").get("entity")
        volumes = data["details"].get("mounted_pvc_list")
        try:
            jupyter_token = data["details"].get("created_template").get("jupyter_token")
        except KeyError:
            jupyter_token = None
        pod_url = data["details"].get("created_template").get("pod_url")
        # TODO bedzie wiecej entity jupyterowych
        if entity == "tensorflow-jupyter":
            return f"OK! {entity} Pod {name} has been successfully created! Mounted volumes: {volumes}\nAccessible at: {pod_url}\nJupyter token: {jupyter_token}"
        else:
            return f"OK! {entity} Pod {name} has been successfully created! Mounted volumes: {volumes}"
    else:
        incrementMetric("compute.create.error")
        error = compute_create_error_parser(data)
        return error


def compute_delete_error_parser(error: dict) -> str:
    """Function that pases error from API for compute delete command.

    :param error: Dict containing error message and further info from API.
    :type error: dict
    :return: String or dict depending on error.
    :rtype: str or dict
    """
    try:
        if error["reason"] == "NOT_DELETED_ANYTHING_IN_COMPUTE_DELETE":
            return f"ERROR! Pod with name {error['details']['name']} does not exist."
    except KeyError:
        return "An unecpected error occured. Please try again, or contact support at support@comtegra.pl."
    return error


def compute_delete_response(response: requests.Response) -> str:
    """Create response string for compute delete command.

    :param response: dict object from API response.
    :type response: requests.Response
    :return: Response string.
    :rtype: str
    """
    if response.status_code == 500:
        return "Internal Server Error"
    data = json.loads(response.text)

    if response.status_code == 200:
        namespace = data["details"].get("namespace")
        name = data["details"].get("deleted_service").get("name")
        compute_delete_telemetry_shot_ok(namespace=namespace)

        return (
            f"OK! Pod {name} successfully deleted"
            if name is not None
            else "Pod does not exist"
        )
    else:
        incrementMetric("compute.delete.error")
        error = compute_delete_error_parser(data)
        return error


def compute_create_telemetry_shot_ok(namespace: str):
    """Function that sends telemetry for compute create command."""

    incrementMetric(f"{namespace}.compute.create.ok")
    changeGauge(f"{namespace}.compute.count", 1)


def compute_delete_telemetry_shot_ok(namespace: str):
    """Function that sends telemetry for compute delete command."""

    incrementMetric(f"{namespace}.compute.delete.ok")
    changeGauge(f"{namespace}.compute.count", -1)
