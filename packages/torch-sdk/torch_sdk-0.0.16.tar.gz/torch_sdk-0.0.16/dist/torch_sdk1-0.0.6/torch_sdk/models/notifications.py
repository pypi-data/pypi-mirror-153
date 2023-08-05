
class Notification:

    def __init__(self, associatedItemId, associatedItemType, createdAt, eventType, id, metadata: dict, title):
        self.title = title
        self.metadata = metadata
        self.id = id
        self.eventType = eventType
        self.createdAt = createdAt
        self.associatedItemType = associatedItemType
        self.associatedItemId = associatedItemId

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Notification({self.__dict__})"


class Incident:

    def __init__(self, associatedItemId, associatedItemType, id, metadata: dict, raisedAt, resolver, sentTo, title, type):
        self.type = type
        self.title = title
        self.sentTo = sentTo
        self.resolver = resolver
        self.raisedAt = raisedAt
        self.metadata = metadata
        self.id = id
        self.associatedItemType = associatedItemType
        self.associatedItemId = associatedItemId

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Incident({self.__dict__})"