#Datasource APIs

Torch SDK has full access on catalog APIs as well. Using torch sdk, one can create datasource and version it with associated assets, relations.
##### Create Virtual Datasource 
Torch sdk has access to create or update existing datasource. Torch has support for virtual datasource as well for ML purpose and some non-virtual/real as well for example relational databases, file based databases et cetera. To create datasource, source type details are required. To get all source types supported in torch, use `get_all_source_types()` method.
```python
from torch_sdk.models.datasource import CreateDataSource, SourceType

# get connection types available in torch
connection_types = torch_client.get_connection_types()

datasource = CreateDataSource(
    name='Feature_bag_datasource_sdk',
    sourceType=SourceType(21, 'FEATURE_BAG'),
    description='feature bag assembly creation using python sdk',
    isVirtual=True
)
datasource_response = torch_client.create_datasource(datasource)
```

##### Create Non-virtual Datasource
Torch has support for more 15+ datasource crawling support. In order yo create a datasource, first create connection along with available analytics pipeline available. 
Then, create datasource with required parameters.

```python

# get all analysis pipelines
torch_client.list_all_analysis_pipelines()
# get pipeline by id
analysis_pipeline = torch_client.get_analysis_pipeline(analysis_pipeline_id)

# connections : list all connections
connection_list = torch_client.list_all_connections()

# create a connection. Make sure proper connection type id has been passed
create_conn_obj = CreateConnection(
    name='mysql_connection_sdk',
    description='create connection from torch sdk',
    connection_type_id=12,
    analytics_pipeline_id=analysis_pipeline.id,
    properties=[ConfigProperty(key='jdbc.url', value='jdbc:postgresql://localhost:5432/'),
                ConfigProperty(key='jdbc.user', value='admin'),
                ConfigProperty(key='jdbc.password', value='admin')]
)
created_conn = torch_client.create_connection(create_conn_obj)

# update connection
update_conn_obj = CreateConnection(
    name='mysql_connection_sdk',
    description='create connection from torch sdk',
    connection_type_id=12,
    analytics_pipeline_id=1,
    properties=[ConfigProperty(key='jdbc.url', value='jdbc:postgresql://localhost:5432/'),
                ConfigProperty(key='jdbc.user', value='admin'),
                ConfigProperty(key='jdbc.password', value='admin')]
)
updated_conn = torch_client.update_connection(update_connection=update_conn_obj)

# test connection - whether parameters are valid or not.  
check_conn_status = torch_client.check_connection(update_conn_obj)

# get asset connection
connection = torch_client.get_connection(name='mysql_connection_sdk')

# delete connection
torch_client.delete_connection(id=connection.id)

# create datasource
datasource = CreateDataSource(
    name='snowflake_ds_local',
    sourceType=SourceType(5, 'SNOWFLAKE'),
    description='snowflake schema',
    connectionId=9,
    configProperties=[ConfigProperty(key='jdbc.warehouse', value='COMPUTE_WH'),
                      ConfigProperty(key='databases.0', value='FINANCE')]
)
ds_res = torch_client.create_datasource(datasource)
# get datasource
ds_res = torch_client.get_datasource('snowflake_ds_local')

#  update datasource
datasource = CreateDataSource(
    name='snowflake_ds_local',
    sourceType=SourceType(5, 'SNOWFLAKE'),
    description='snowflake schema',
    connectionId=9,
    configProperties=[ConfigProperty(key='jdbc.warehouse', value='COMPUTE_WH'),
                      ConfigProperty(key='databases.0', value='CRAWLER_DB1')]
)
ds_res = ds_res.update_datasource(datasource)

# get root assets
ds_res.get_root_assets()


```

##### Create New Version Of Datasource
Torch sdk can version the datasource as well. Torch sdk can initiate new version the datasource and return latest instance of it. It has also method to get current latest snapshot version.
```python
# get data source
datasource_response = torch_client.get_datasource('Feature_bag_datasource')

# create new version of the datasource
new_snapshot_version = datasource_response.initialise_snapshot(uid='Habcfc38-9daa-4842-b008-f7fb3dd8439a')

# get current snapshot data
current_snapshot_version = datasource_response.get_current_snapshot()

# list all snapshots for a datasource
snapshots = datasource.list_all_snapshots()

# list snapshots in torch for all datasources
snapshots = torch_client.list_all_snapshots()
```
##### Create Asset And Relations B/w Them
Create/Update assets and relations between them.
With use of the torch sdk, user can create assets in datasource and can also define relations between assets. To get asset types supported in torch, use `get_asset_types()` method. Torch sdk has methods to get existing relations and assets in the given datasource.
```python
from torch_sdk.models.create_asset import AssetMetadata

# get asset by id/uid
datasource_response = torch_client.get_datasource('Feature_bag_datasource')

# discover all the assets
discover_res = torch_client.discover()

# create assets
asset_1 = datasource_response.create_asset(uid='Feature_bag_datasource.feature_1',
                                            metadata=[AssetMetadata('STRING', 'abcd', 'pqr', 'sds')],
                                            asset_type_id=22,
                                            description='feature 1 asset.',
                                            name='car feature'
                                                )
asset_2 = datasource_response.create_asset(uid='Feature_bag_datasource.feature_2',
                                            metadata=[AssetMetadata('STRING', 'abcd', 'pqr', 'sds')],
                                            asset_type_id=22,
                                            description='feature asset 2',
                                            name='bike feature'
                                                )

# create asset relation
toAssetUUID = 'postgres-assembly-5450.ad_catalog.ad_catalog.qrtz_simple_triggers'
relationType = RelationType.SIBLING
asset_relation_1_to_2 = asset_1.create_asset_relation(relation_type=relationType, to_asset_uuid=toAssetUUID)

# get asset by id/uid
asset = datasource_response.get_asset(id=1)
asset = datasource_response.get_asset(uid='Feature_bag_datasource.feature_1')


# get related and child asset
relations = asset.get_related_assets()
child_assets = asset.get_child_assets()

# delete an asset
datasource_response.delete_asset(id=asset.id)

```
##### Asset's tags, labels, annotations and activities
User can add tags, labels and also update annotation and activities of the asset using sdk.
To give alias to an asset, add label with `alias` key and value as an alias name.
Tags and labels can be used to filter out asset easily.
```python

# asset metadata
asset = torch_client.get_asset(id=asset_id)
metadata = [AssetMetadata('STRING', 'key', 'source', 'value'), AssetMetadata('STRING', 's3_location', 'AWS_S3', 's3://aws/path/test/logs')]
# update and get metadata of an asset
asset.update_asset_metadata(metadata)
asset.get_asset_metadata()

# get all tags
tags = torch_client.get_tags()
# update data protection for tag
torch_client.update_data_protection(tag='asset_tag', is_protected=True)
# delete tag 
torch_client.delete_tag(tag='asset_tag')

# get an asset by id
asset = datasource.get_asset(id=asset_id)

# get asset tags
tags = asset.get_asset_tags()
# add tag asset
tag_add = asset.add_asset_tag(tag='asset_tag')
# remove asset
tag_rm = asset.remove_asset_tag(tag='asset_tag')

# get asset activities
activty = asset.get_asset_activity()

# get asset comments
comments = asset.get_asset_comment()

# add asset labels
labels = asset.add_asset_labels(labels = ['teamtorch', 'comp:adinc'])
# get asset labels
labels = asset.get_asset_labels()

# update asset annotation
annotation = asset.update_asset_annotation(annotation='this asset is created and accessed from torch sdk')

# start watching asset
start_watch = asset.start_watch()
# stop watching asset
asset.stop_watch()


# classification configs : get all, create, update, delete
configs = torch_client.list_all_classification_configurations()
create_config = ClassificationConfig(
    name='CCV', protectedData=False, classification='regex',
    classificationType='card', enabled= False, description='Card CCV Checking with regex',
    defaultValue='^\\d{3}$', value='^\\d{4}$'
)

config_created = torch_client.create_classification_configuration(create_config)

config = torch_client.get_classification_configuration(name='CCV')

update_config = ClassificationConfig(
    id=config.id, name='CCV', protectedData=False, classification='regex',
    classificationType='card', enabled= False,
    description='Card CCV Checking with regex',
    defaultValue='^\\d{3}$', value='^\\d{3}$'
)

config_updated = torch_client.update_classification_configuration(update_config)

torch_client.delete_classification_configuration(name='CCV')

```

##### Crawler Operations
User can start and restart crawler as well check for running crawler status too.
```python
# start a crawler
datasource.start_crawler()

# get running crawler status
datasource.get_crawler_status()

# restart a crawler
datasource.restart_crawler()
```

##### User And API Keys Management
Torch user and API key management support. API keys can be used for pipelines creations. Also, for API authentication too. 
Settings can be set up via sdk. (Settings has only an update and a read permission)
```python

# get user by name/id
user = torch_client.get_user(user_id=id)
user = torch_client.get_user(username='admin')


# api keys: create, get, delete
keys = torch_client.create_api_key()
torch_client.get_api_keys()
torch_client.delete_api_key(keys.accessKey)

# notifications and incidents in torch
torch_client.get_notifications()
torch_client.get_incidents()

# setting groups: get all
setting_groups = torch_client.list_setting_groups()
# get setting available in each group by group name
settings = torch_client.find_settings_by_group(setting_group_name= 'data_protection')
# get setting key
setting = torch_client.get_setting(key='notification.channels.email.toEmail')
# update setting key value
updated_setting = torch_client.update_setting_value(key='data.protection.enabled', value="true")
# reset setting value
reset_setting_value = torch_client.reset_setting_value(key='data.protection.enabled')

```

##### Trigger policies, Profiling and sampling of an asset
Crawled assets can be profiled and sampled with use of spark jobs running on the livy. 
Furthermore, Created policies (Recon + DQ) can be triggered too.
```python

# get all auto profile configs
torch_client.get_all_auto_profile_configurations()
# get auto profile for a datasource
ds_res.get_auto_profile_configuration()
# remove auto profile for a datasource
ds_res.remove_auto_profile_configuration()

# profile an asset, get profile req details, cancel profile, autotag profile
profile_res = asset.profile_asset(profiling_type= ProfilingType.SAMPLE, job_type=JobType.MINI_PROFILE)

profile_req_details = profile_res.get_profile_request_details()

cancel_profile_res = profile_res.cancel_profile()

profile_res = asset.get_profile_status()

autotag_res = asset.auto_tag_asset()

profile_req_details_by_req_id = asset.get_profile_request_details(req_id= profile_req_details.id)

# sample data
sample_data = asset.sample_data()



# rule execution and ops

enable_rule = torch_client.enable_rule(rule_id=rule_id)
disable_rule = torch_client.disable_rule(rule_id=rule_id)

# trigger dq rule
execute_dq_rule = torch_client.execute_dq_rule(rule_id=rule_id)
get_dq_execution_details = torch_client.get_dq_rule_execution_details(execution_id=rule_id)

# trigger reconciliation rule
execute_reconciliation_rule = torch_client.execute_reconciliation_rule(rule_id=rule_id)
get_recon_exe_details = torch_client.get_reconciliation_rule_execution_details(execution_id=get_dq_execution_details.id)

# cancel rule execution job
cancel_rule = torch_client.cancel_rule_execution(execution_id=execute_dq_rule.id)

```