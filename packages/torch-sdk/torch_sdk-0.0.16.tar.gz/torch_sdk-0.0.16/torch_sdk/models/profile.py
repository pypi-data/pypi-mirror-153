from enum import Enum


class Profile:

    def __init__(self, assetId, createdAt, id, jobId, profilingType, sparkClusterContext, status, updatedAt, rows=None,
                 totalRows=None, jobType=None, autoProfileId=None, profileDataAvailable=None, marker=None,
                 profiledData=None, error=None, client=None, **kwargs):
        self.client = client
        self.autoProfileId = autoProfileId
        self.profileDataAvailable = profileDataAvailable
        self.jobType = jobType
        self.updatedAt = updatedAt
        self.status = status
        self.sparkClusterContext = sparkClusterContext
        self.rows = rows
        self.profilingType = profilingType
        self.profiledData = profiledData
        self.marker = marker
        self.jobId = jobId
        self.id = id
        self.error = error
        self.createdAt = createdAt
        self.assetId = assetId
        self.totalRows = totalRows

    def __repr__(self):
        return f"Profile({self.__dict__})"

    def cancel_profile(self):
        return self.client.cancel_profile(self.id)

    def get_profile_request_details(self):
        return self.client.get_profile_request_details(asset_id=self.assetId, req_id=self.id)


class AutoProfileConfiguration:

    def __init__(self, assemblyId, assemblyName, createdAt, updatedAt, enabled, schedule, parallelizationCount, id=None,
                 includeList=None, excludeList=None, **kwargs):
        self.assemblyId = assemblyId
        self.assemblyName = assemblyName
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.enabled = enabled
        self.schedule = schedule
        self.parallelizationCount = parallelizationCount
        self.id = id
        if isinstance(includeList, list):
            self.includeList = list(includeList)
        else:
            self.includeList = includeList

        if isinstance(excludeList, dict):
            self.excludeList = list(excludeList)
        else:
            self.excludeList = excludeList

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"AutoProfileConfiguration({self.__dict__})"


class ProfilingType(Enum):
    SAMPLE = 'SAMPLE'
    FULL = 'FULL'
    INCREMENTAL = 'INCREMENTAL'


class JobType(Enum):
    PROFILE = 'profile'
    MINI_PROFILE = 'mini-profile'
    # FULL = 'autotag'


class ProfileRequest:

    def __init__(self, id, status, createdAt, updatedAt, client=None, **kwargs):
        self.client = client
        self.updatedAt = updatedAt
        self.createdAt = createdAt
        self.status = status
        self.id = id

    def __repr__(self):
        return f"ProfileRequest({self.__dict__})"

    def cancel_profile(self):
        return self.client.cancel_profile(self.id)
