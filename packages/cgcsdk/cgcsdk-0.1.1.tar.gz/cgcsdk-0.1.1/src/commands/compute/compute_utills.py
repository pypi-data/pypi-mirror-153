import click


def list_get_main_container(container_list: list, entity: str) -> dict:
    for container in container_list:
        try:
            if container["name"] == entity:
                return container
        except KeyError:
            click.echo("something went wrong")
    return None


def list_get_mounted_volumes(volume_list: list) -> str:
    volume_name_list = []
    for volume in volume_list:
        volume_type = volume.get("type")
        if volume_type == "PVC":
            volume_name = volume.get("name")
            volume_name_list.append(volume_name)
    volumes_mounted = (
        ", ".join(volume_name_list) if len(volume_name_list) != 0 else "none"
    )
    return volumes_mounted


def list_get_pod_list_to_print(pod_list: list) -> list:
    pod_list_to_print = []
    for pod in pod_list:
        try:
            labels = pod["labels"]
            pod_name = labels["app-name"]
            pod_type = labels["entity"]
            status = pod["status"]
            #! Nie każdy pod ma gpu type
            try:
                gpu_type = labels["gpu-label"]
            except KeyError:
                gpu_type = "none"
            gpu_count = (
                labels.get("gpu-count") if labels.get("gpu-count") is not None else 0
            )
            try:
                pod_url = labels["pod_url"]
            except KeyError:
                pod_url = "none"
            try:
                jupyter_token = labels["jupyter-token"]
            except KeyError:
                jupyter_token = "none"

            main_container = list_get_main_container(pod["containers"], pod_type)

            limits = main_container["resources"]["limits"]

            cpu = limits.get("cpu") if limits is not None else 0
            ram = limits.get("memory") if limits is not None else "0Gi"

            volumes_mounted = list_get_mounted_volumes(main_container["mounts"])

            row_list = [
                pod_name,
                pod_type,
                status,
                volumes_mounted,
                cpu,
                ram,
                gpu_type,
                gpu_count,
                pod_url,
                jupyter_token,
            ]
            pod_list_to_print.append(row_list)
        except KeyError as error:
            click.echo(
                f"Something went wrong with pod {pod.get('name')}. KeyError: {error}"
            )
        except:
            click.echo(f"There is somekind of error: {error}")
    return pod_list_to_print
