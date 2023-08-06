def get_formatted_volume_list_and_total_size(list_of_volumes: list):
    list_to_print = []
    total_size = 0
    for volume in list_of_volumes:
        name = volume["name"]
        used = volume["used"]
        size = volume["size"]
        access_types = ", ".join(volume["access_types"])
        all_mounted_to = ", ".join(volume["mounted_to"])
        total_size += int("".join(filter(str.isdigit, size)))
        row_list = [name, used, size, access_types, all_mounted_to]
        list_to_print.append(row_list)
    return list_to_print, total_size
