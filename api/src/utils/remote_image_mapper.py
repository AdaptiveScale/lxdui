
def remote_images_list(images):
    response = []
    aliases = [alias[20:] for alias in images['metadata']]
    for alias in aliases:
        split_alias = alias.split('/')
        if len(split_alias) > 2:
            name = split_alias[0].__str__()
            distribution = split_alias[1].__str__()
            architecture = split_alias[2].__str__()

            image = {
                'name': name,
                'distribuion': distribution,
                'architecture': architecture,
                'image': alias
            }

            if image not in response: response.append(image)

    return response