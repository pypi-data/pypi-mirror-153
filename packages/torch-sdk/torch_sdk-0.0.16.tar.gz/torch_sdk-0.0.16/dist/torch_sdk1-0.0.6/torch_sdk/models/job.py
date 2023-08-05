from dataclasses import dataclass


@dataclass
class JobMetadata:
    """
    Description:
        job metadata.

    :param owner : (String) owner of the pipeline
    :param team: (String) team of the owner
    :param codeLocation: (String) location of the code
    """
    owner: str = None
    team: str = None
    codeLocation: str = None


@dataclass
class Dataset:
    """
        Description:
            data set object would be input/output for the job.
        :param source: (String) data source name in the torch catalog
        :param asset_uid: (String) asset uid. - asset path from it's root
    """
    source: str = None
    asset_uid: str = None


class CreateJob:
    #  inputs : List[Dataset] = None, outputs : List[Dataset] = None
    def __init__(self, uid: str, name: str, pipelineSnapshot: str, description: str = None, inputs=None, outputs=None, meta: JobMetadata = None, **context):
        """
        Description:
            create job class used to create job in torch catalog
        :param uid: uid of the job. it should be unique for the job
        :param name: name of the job
        :param description: desc of the job
        :param inputs: (list[Dataset]) input for the job
        :param outputs: (list[Dataset]) output for the job
        :param meta: job metadata
        :param pipeline: pipeline object for which you want to add a job
        :param context: context
        """
        if outputs is None:
            outputs = []
        if inputs is None:
            inputs = []
        self.uid = uid
        self.name = name
        self.pipelineSnapshot = pipelineSnapshot
        self.description = description
        if meta is not None:
            self.meta = JobMetadata(meta.owner, meta.team, meta.codeLocation)
        self.inputs = inputs
        self.outputs = outputs
        self.context = context

    def __eq__(self, other):
        return self.uid == other.uid

    def __repr__(self):
        return f"Job({self.uid!r})"


class Job:
    def __init__(self,
                 uid: str,
                 id: int = None,
                 name: str = None,
                 description: str = None,
                 meta=None,
                 type: str = None,
                 assetId: int = None,
                 pipelineId: int = None, context=None, **kwrgs):
        """
        Description:
            Job of the pipeline.
        :param uid: uid of the job
        :param id: id of the job
        :param name: name of the job
        :param description: desc of the job
        :param meta: metadata of the job
        :param type: type of the job.
        :param assetId: asset id associated with job
        :param pipelineId: pipeline id in which we've configured the job
        :param context: context data for the job
        :param kwrgs: additional args
        """
        self.uid = uid
        self.name = name
        self.description = description
        self.type = type
        if isinstance(meta, dict):
            self.meta = JobMetadata(**meta)
        else:
            self.meta = meta
        self.context = context
        self.id = id
        self.assetId = assetId
        self.pipelineId = pipelineId

    def __eq__(self, other):
        return self.uid == other.uid

    def __repr__(self):
        return f"JobResponse({self.__dict__})"
