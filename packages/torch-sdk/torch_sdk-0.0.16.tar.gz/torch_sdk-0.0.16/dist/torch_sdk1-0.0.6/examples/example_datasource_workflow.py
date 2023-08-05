from torch_sdk.initialiser import torch_client_credentials
from torch_sdk.models.asset import RelationType
from torch_sdk.models.datasource import CreateDataSource, SourceType
from torch_sdk.torch_client import TorchClient
from torch_sdk.models.create_asset import AssetMetadata

torchClient = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")

datasource = CreateDataSource(
    name='Feature_bag_datasource_sdk_3',
    sourceType=SourceType(21, 'FEATURE_BAG'),
    description='feature bag assembly creation using python sdk',
    isVirtual=True,
    # name= 'aws_athena_ds_sdk',
    # sourceType= SourceType(16, 'AWS_ATHENA'),
    # description= 'creation of assembly using sdk',
    # connectionId= 1,
    # configProperties= [ ConfigProperty(key= 's3.location', value= 's3://ad-redshift-data/athena_result/s3')]
)

datasourceResponse = torchClient.create_datasource(datasource)
print('Newly created datasource: ', datasource)

newSnapshotVersion = datasourceResponse.initialise_snapshot(uid='NIffc38-9daa-4842-b008-f7fb3dd8439a')
print('New snapshot version created : ', newSnapshotVersion)

# getCurrentVersion = datasourceResponse.get_current_snapshot()
# print('getting current version of datasource : ', getCurrentVersion)

metadata = [AssetMetadata('STRING', 'abcd', 'pqr', 'sds'), AssetMetadata('STRING', 'abcdq', 'pqrq', 'sqds'), AssetMetadata('STRING', 'abcddq', 'pqrqd', 'sqdds')]

assetResponse = datasourceResponse.create_asset(uid='Feature_bag_datasource_sdk.feature_sdk_1',
                                                metadata=metadata,
                                                asset_type_id=22,
                                                description='Test asset creation',
                                                name='feature_sdk_1'
                                                )
print('Newly created asset response : ', assetResponse)

# fromAssetUUID = 'Feature_bag_datasource_sdk.feature_sdk_1'
# toAssetUUID = 'postgres-assembly-5450.ad_catalog.ad_catalog.qrtz_simple_triggers'
# relationType = RelationType.SIBLING
#
# assetRelationResponse = assetResponse.create_asset_relation(relation_type= relationType, to_asset_uuid= toAssetUUID)
# print('Newly created asset relation', assetRelationResponse)

delete_asset = datasourceResponse.delete_asset(id=9523)
print(delete_asset)
