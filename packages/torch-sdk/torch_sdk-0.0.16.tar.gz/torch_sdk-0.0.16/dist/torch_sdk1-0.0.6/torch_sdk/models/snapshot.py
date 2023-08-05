from enum import Enum


class AssociatedItemType(Enum):
    """
        Description:
            associated item type for versioning
        assembly -> data source in torch
        pipeline -> pipeline/topology
    """
    ASSEMBLY = 1
    PIPELINE = 2


class SnapshotData:

    def __init__(self, uuid: str, associatedItemType: AssociatedItemType, associatedItemId: int, status: str = None,
                 createdAt=None, updatedAt=None, id: int = None, **kwrgs):
        """
            Description:
                Class to represent version of the entities
        :param uuid: universal uid that displays the version
        :param associatedItemType: associated item type can be assembly or pipeline.
        :param associatedItemId: associated item id like datasource id for assembly. pipeline id for pipeline
        :param status: status of the snapshot version
        :param createdAt: creation time
        :param updatedAt: updated time
        :param id: id for the snapshot
        """
        self.uuid = uuid
        self.associatedItemType = associatedItemType
        self.associatedItemId = associatedItemId
        if createdAt is not None:
            self.status = status
            self.createdAt = createdAt
            self.updatedAt = updatedAt
            self.id = id

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __repr__(self):
        return f"SnapshotData({self.__dict__})"
