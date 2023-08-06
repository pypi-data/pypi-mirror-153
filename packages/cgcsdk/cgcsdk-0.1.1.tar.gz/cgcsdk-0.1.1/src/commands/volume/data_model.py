def volume_create_payload_validator(name, access, size, disk_type):
    """
    Create payload for volume creation.
    """
    payload = {
        "name": name,
        "access_type": access,
        "size": size,
        "disks_type": disk_type,
        "auto_mount": "true",
    }
    return payload


def volume_delete_payload_validator(name, force_delete):
    """
    Create payload for volume deletion.
    """
    payload = {
        "name": name,
        "force_delete": force_delete,
    }

    return payload


def volume_mount_payload_validator(name, target, target_template_type, mount_path):
    """
    Create payload for volume mount.
    """
    payload = {
        "name": name,
        "target_template_type": target_template_type,
        "target_template_name": target,
        "start_mount_path": mount_path,
    }

    return payload


def volume_umount_payload_validator(name):
    """
    Create payload for volume umount.
    """
    payload = {"name": name}

    return payload
