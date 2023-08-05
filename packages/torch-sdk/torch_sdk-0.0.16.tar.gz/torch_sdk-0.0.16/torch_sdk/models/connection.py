from enum import Enum


class ConnectionType:

    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"ConnectionType({self.__dict__})"


class AnalysisPipeline:

    def __init__(self, id, name, accessKey, createdAt, updatedAt, url, externalUrl, description, hbaseEnabled,
                 hdfsEnabled,
                 hiveEnabled, **kwargs):
        self.name = name
        self.accessKey = accessKey
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.url = url
        self.id = id
        self.externalUrl = externalUrl
        self.description = description
        self.hbaseEnabled = hbaseEnabled
        self.hdfsEnabled = hdfsEnabled
        self.hiveEnable = hiveEnabled

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"AnalysisPipeline({self.__dict__})"


class ConfigProperty:

    def __init__(self, key, value, id=None, **kwargs):
        self.key = key
        self.value = value
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"ConfigProperty({self.__dict__})"


class Connection:

    def __init__(self, name, connectionType, createdAt, updatedAt, analyticsPipeline, configuration, assemblyCount=0,
                 description=None,
                 id=None, **kwargs):
        self.name = name
        self.configuration = configuration
        self.connectionType = connectionType
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.assemblyCount = assemblyCount
        self.description = description
        self.id = id
        if isinstance(connectionType, dict):
            self.connectionType = ConnectionType(**connectionType)
        else:
            self.connectionType = connectionType
        if isinstance(analyticsPipeline, dict):
            self.analyticsPipeline = AnalysisPipeline(**analyticsPipeline)
        else:
            self.analyticsPipeline = analyticsPipeline

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"Connection({self.__dict__})"


class CreateConnection:

    def __init__(self, name, connection_type_id, analytics_pipeline_id, properties, description=None):
        self.name = name
        self.connectionTypeId = connection_type_id
        self.analyticsPipelineId = analytics_pipeline_id
        self.properties = properties
        self.description = description

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"CreateConnection({self.__dict__})"


class ConnectionCheckStatus(Enum):
    SUCCESS = 1
    FAILURE = 2


class ConnectionCheck:

    def __init__(self, message, status, **kwargs):
        self.message = message
        self.status = status

    def __repr__(self):
        return f"ConnectionCheckResponse({self.__dict__})"
