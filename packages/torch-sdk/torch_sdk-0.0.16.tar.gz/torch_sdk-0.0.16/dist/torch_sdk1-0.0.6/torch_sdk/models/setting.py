

class SettingGroup:

    def __init__(self, id, name, displayName, description, **kwargs):
        self.id = id
        self.name = name
        self.displayName = displayName
        self.description = description

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Setting-Group({self.__dict__})"


class Setting:

    def __init__(self, id, key, displayName, value, defaultValue, isReadOnly: bool, valueType, settingGroupId, description = None, **kwargs):
        self.id = id
        self.key = key
        self.displayName = displayName
        self.value = value
        self.defaultValue = defaultValue
        self.isReadOnly = isReadOnly
        self.valueType = valueType
        self.settingGroupId = settingGroupId
        self.description = description

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Setting({self.__dict__})"