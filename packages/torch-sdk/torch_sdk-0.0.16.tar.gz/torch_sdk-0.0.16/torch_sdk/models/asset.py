from dataclasses import asdict

from torch_sdk.errors import TorchSdkException
from torch_sdk.models.profile import ProfilingType, JobType
from torch_sdk.models.assetType import AssetType
from torch_sdk.models.create_asset import RelationType, CreateAssetRelation, AssetMetadata
from torch_sdk.models.datasource import DataSource, DatasourceSourceType


class AssetRelation:

    def __init__(self,
                 fromAssetId: str,
                 toAssetId: str,
                 currentSnapshot: str,
                 snapshots,
                 relation: RelationType,
                 hasSubRelations: bool = False,
                 id: int = None,
                 isDeleted: bool = None,
                 metadata=None,
                 **kwargs):
        """
            Description:
                Asset relation class
        :param fromAssetId: source asset id
        :param toAssetId: sink asset id
        :param currentSnapshot: current version of the asset relation
        :param snapshots: version list
        :param id: asset relation id
        :param isDeleted: isDeleted or not in newer version
        :param relation: (RelationType) relation type
        :param metadata: (List[AssetMetadata]) metadata of the asset relation
        :param hasSubRelations: (bool) has sub relations or not
        """
        self.fromAssetId = fromAssetId
        self.toAssetId = toAssetId
        self.currentSnapshot = currentSnapshot
        self.snapshots = snapshots
        self.id = id
        self.isDeleted = isDeleted
        self.relation = relation
        self.metadata = metadata
        self.hasSubRelations = hasSubRelations

    def __eq__(self, other):
        return self.toAssetId == other.toAssetUUID and self.fromAssetId == other.fromAssetUUID

    def __repr__(self):
        return f"AssetRelation({self.__dict__})"


class ChildType:

    def __init__(self, canProfile, canSample, id, name):
        self.canProfile = canProfile
        self.canSample = canSample
        self.id = id
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"ChildType({self.__dict__})"


class ChildAsset:
    def __init__(self, assetId, isCustom, name, parentId=None, alias=None, childType=None):
        self.assetId = assetId
        self.isCustom = isCustom
        self.name = name
        self.parentId = parentId
        self.alias = alias
        if isinstance(childType, dict):
            self.datasource = ChildType(**childType)
        else:
            self.datasource = childType

    def __eq__(self, other):
        return self.assetId == other.assetId

    def __repr__(self):
        return f"ChildAsset({self.__dict__})"


class Metadata:

    def __init__(self, assetId, createdAt, updatedAt, currentSnapshot, id, items, metaDataHash, snapshots=None):
        self.assetId = assetId
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.currentSnapshot = currentSnapshot
        self.id = id
        self.metaDataHash = metaDataHash
        if isinstance(items, list):
            items_list = list(items)
            asset_metadata = []
            for i in items_list:
                asset_mt = AssetMetadata(**i)
                asset_metadata.append(asset_mt)
            self.items = asset_metadata
        else:
            self.items = items
        if isinstance(snapshots, list):
            self.snapshots = list(snapshots)
        else:
            self.snapshots = snapshots

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"Metadata({self.__dict__})"


class Asset:

    def __init__(self,
                 alias=None,
                 assembly=None,
                 assetType: AssetType = None,
                 createdAt=None,
                 currentSnapshot=None,
                 description=None,
                 id=None,
                 isCustom=None,
                 isDeleted=None,
                 name=None,
                 parentId=None,
                 snapshots=None,
                 sourceType=None,
                 uid=None,
                 updatedAt=None,
                 client=None,
                 **kwargs
                 ):
        """
            Description:
                Asset class
        :param alias: alias of the asset
        :param assembly: (Datasource) data source details
        :param assetType: type of the asset
        :param createdAt: creation time of the asset
        :param currentSnapshot: current version of the asset
        :param description: desc of the asset
        :param id: asset id
        :param isCustom: is custom asset or not
        :param isDeleted: is deleted or not in current version of the datasource
        :param name: name of the asset
        :param parentId: parent id of the asset
        :param snapshots: version list
        :param sourceType: source type of the asset's datasource
        :param uid: uid of the asset
        :param updatedAt: updated time of the asset
        """
        self.alias = alias
        self.createdAt = createdAt
        self.currentSnapshot = currentSnapshot
        self.description = description
        self.id = id
        self.isCustom = isCustom
        self.isDeleted = isDeleted
        self.name = name
        self.parentId = parentId
        self.snapshots = snapshots
        self.uid = uid
        self.updatedAt = updatedAt
        if isinstance(assembly, dict):
            self.datasource = DataSource(**assembly)
        else:
            self.datasource = assembly
        if isinstance(assetType, dict):
            self.assetType = AssetType(**assetType)
        else:
            self.assetType = assetType
        if isinstance(sourceType, dict):
            self.sourceType = DatasourceSourceType(**sourceType)
        else:
            self.sourceType = sourceType

        # self.datasource = assembly
        # self.sourceType = sourceType

        self.client = client

    def __repr__(self):
        return f"Asset({self.__dict__})"

    # convert asset relation to dict type
    def _convert_asset_relation_to_dict(self, asset_relation: CreateAssetRelation):
        """
        Description:
            Convert CreateAssetRelation class instance to dict type
        :param assetRelation: CreateAssetRelation class instance
        :return: dict form of CreateAssetRelation class instance
        """
        payload = asset_relation.__dict__
        payload['relationType'] = asset_relation.relationType.name
        asset_relation_payload = {'data': payload}
        return asset_relation_payload

    # create relation between asset
    def create_asset_relation(self, to_asset_uuid: str, relation_type: RelationType,
                              snapshots=None):
        """
        Description:
            used to create relation between any 2 existing assets
        :param snapshots:
        :param relation_type:
        :param to_asset_uuid:
        :return: created AssetRelation class instance
        """
        if snapshots is None:
            snapshots = [self.currentSnapshot]
        asset_relation = CreateAssetRelation(
            fromAssetUUID=self.uid,
            assemblyId=self.datasource.id,
            toAssetUUID=to_asset_uuid,
            relationType=relation_type,
            currentSnapshot=self.currentSnapshot,
            snapshots=snapshots
        )
        payload = self._convert_asset_relation_to_dict(asset_relation)
        return self.client.create_asset_relation(payload)

    def get_related_assets(self):
        return self.client.get_related_assets(self.id)

    def get_child_assets(self):
        return self.client.get_child_assets(self.id)

    def start_watch(self):
        return self.client.start_watch(self.id)

    def stop_watch(self):
        return self.client.stop_watch(self.id)

    def get_asset_tags(self):
        return self.client.get_asset_tags(self.id)

    def get_asset_activity(self):
        return self.client.get_asset_activity(self.id)

    def get_asset_comment(self):
        return self.client.get_asset_comment(self.id)

    def add_asset_tag(self, tag):
        payload = {
            "assetTag": {
                "name": tag,
                "assetId": self.id,
                "autoTagged": False
            }
        }
        return self.client.add_asset_tag(self.id, payload)

    def remove_asset_tag(self, tag):
        tags = self.client.get_asset_tags(self.id)
        tag_id = None
        for tg in tags:
            if tg.name == tag:
                tag_id = tg.tagId
        if tag_id is None:
            raise TorchSdkException('Tag not found for the asset. Tag doesnt exists')
        return self.client.remove_asset_tag(self.id, tag_id)

    def add_asset_labels(self, labels: []):
        """
        Description:
            add asset labels.
            To give alias add 'alias:alias_name'.
            label key and value should be simple string. It should not contain any special characters in it.
        :param labels: list of strings. format : 'key:value'. Ex. labels : ['key1:value1', 'key2:value2']
        :return:
        """
        lbls = []
        for label in labels:
            count = label.count(':')
            if count != 1:
                raise TorchSdkException(
                    f'Invalid input label string {label}. label key and value should be simple string. It should not '
                    f'contain any special characters in it.')
            lbl = label.split(':')
            label_dict = {
                'key': lbl[0],
                'value': lbl[1]
            }
            lbls.append(label_dict)
        payload = {
            'labels': lbls
        }
        return self.client.add_asset_labels(self.id, payload)

    def get_asset_labels(self):
        return self.client.get_asset_labels(self.id)

    def update_asset_annotation(self, annotation: str):
        payload = {
            'annotation': annotation
        }
        return self.client.update_asset_annotation(self.id, payload)

    def get_asset_metadata(self):
        return self.client.get_asset_metadata(self.id)

    def update_asset_metadata(self, asset_metadata):
        """
        Description:
            Update asset metadata for a latest snapshot version
        :param asset_metadata: list of AssetMetadata Object
        :return:
        """
        metadata = []
        for md in asset_metadata:
            metadata.append(asdict(md))

        metadata_payload = {
            'data': {
                'items': metadata,
                'currentSnapshot': self.currentSnapshot,
                'snapshots': self.snapshots
            }
        }
        return self.client.update_asset_metadata(self.id, metadata_payload)

    def profile_asset(self, profiling_type: ProfilingType, job_type: JobType = JobType.PROFILE):
        payload = {
            'data': {
                'profilingType': profiling_type.value,
                'jobType': job_type.value
            }
        }
        return self.client.profile_asset(self.id, payload)

    def get_profile_status(self):
        return self.client.get_profile_status(self.id)

    def auto_tag_asset(self):
        payload = {
            'data': {
                'profilingType': ProfilingType.FULL.value,
            }
        }
        return self.client.auto_tag_asset(self.id, payload)

    def sample_data(self):
        return self.client.sample_data(self.id)

    def get_profile_request_details(self, req_id):
        self.client.get_profile_request_details(asset_id=self.id, req_id=req_id)