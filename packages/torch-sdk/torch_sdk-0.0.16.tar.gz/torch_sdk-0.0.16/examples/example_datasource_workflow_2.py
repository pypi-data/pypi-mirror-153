from torch_sdk.initialiser import torch_client_credentials
from torch_sdk.models.asset import RelationType
from torch_sdk.models.datasource import CreateDataSource, SourceType
from torch_sdk.torch_client import TorchClient
from torch_sdk.models.create_asset import AssetMetadata

torch_client = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")

# get data source
datasourceResponse = torch_client.get_datasource('Feature_bag_datasource_sdk_3')
print('Get datasource by name : ', datasourceResponse)

# get asset by id/uid
# get_asset = datasourceResponse.get_asset(id=15382)
# print('Get asset by id ', get_asset)
get_asset_by_uid = datasourceResponse.get_asset(uid='Feature_bag_datasource.feature_no_1')
print('Get asset by uid ', get_asset_by_uid)

newSnapshotVersion = datasourceResponse.initialise_snapshot(uid='H1c38-9daa-4842-b008-f7fb3dd8439a')
print('New snapshot version created : ', newSnapshotVersion)

getCurrentVersion = datasourceResponse.get_current_snapshot()
print('getting current version of datasource : ', getCurrentVersion)

metadata = [AssetMetadata('STRING', 'abcd', 'pqr', 'sds'), AssetMetadata('STRING', 'abcdq', 'pqrq', 'sqds'),
            AssetMetadata('STRING', 'abcddq', 'pqrqd', 'sqdds')]

assetResponse = datasourceResponse.create_asset(uid='Feature_bag_datasource.feature_no_1',
                                                metadata=metadata,
                                                asset_type_id=22,
                                                description='Test asset creation',
                                                name='feature_no_1'
                                                )
print('Newly created asset response : ', assetResponse)

fromAssetUUID = 'Feature_bag_datasource.feature_no_1'
toAssetUUID = 'postgres-assembly-5450.ad_catalog.ad_catalog.qrtz_simple_triggers'
relationType = RelationType.SIBLING

# assetRelationResponse = datasourceResponse.create_asset_relation(from_asset_uuid= fromAssetUUID, relation_type= relationType, to_asset_uuid= toAssetUUID)
# print('Newly created asset relation', assetRelationResponse)

assetRelationResponse = assetResponse.create_asset_relation(relation_type=relationType, to_asset_uuid=toAssetUUID)
print('Newly created asset relation', assetRelationResponse)
