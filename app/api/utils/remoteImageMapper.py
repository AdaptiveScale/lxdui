
def remoteImagesList(images):
    response = []
    aliasesProcessed = []
    aliases = [alias[20:] for alias in images['metadata']]
    for alias in aliases:
        strippedAlias = alias.replace('/default','')
        if strippedAlias not in aliasesProcessed:
            aliasesDetails = alias.split('/')
            if len(aliasesDetails) > 2:
                image = prepRemoteImageObject(strippedAlias, aliasesDetails)
                if image not in response: response.append(image)
            aliasesProcessed.append(strippedAlias)

    return response

def prepRemoteImageObject(alias, aliasesDetails):
    image = {
        'name': aliasesDetails[0].__str__(),
        'distribution': aliasesDetails[1].__str__(),
        'architecture': aliasesDetails[2].__str__(),
        'image': alias
    }

    return image

