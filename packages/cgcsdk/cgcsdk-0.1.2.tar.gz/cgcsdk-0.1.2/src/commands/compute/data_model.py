def compute_create_payload_validator(
    name, entity, cpu, memory, volumes: list, gpu: int, gpu_type: str
):
    """
    Create payload for pod creation.
    """

    payload = {
        "name": name,
        "entity": entity,
        "cpu": cpu,
        "memory": memory,
        "gpu_type": gpu_type,
    }
    if len(volumes) != 0:
        payload["pv_volume"] = volumes
    if gpu != 0:
        payload["gpu"] = gpu
        # TODO Jak backend skonczy to tu bedziemy podawac None a nie string
        if gpu_type == None:
            payload["gpu_type"] = "A100"

    return payload


def compute_delete_payload_validator(name):
    """
    Create payload for pod creation.
    """
    payload = {
        "name": name,
    }
    return payload
