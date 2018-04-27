def getSnapshotData(snapshot):
    return {
        'name': snapshot.name,
        'stateful': snapshot.stateful,
        'createdAt': snapshot.created_at
    }