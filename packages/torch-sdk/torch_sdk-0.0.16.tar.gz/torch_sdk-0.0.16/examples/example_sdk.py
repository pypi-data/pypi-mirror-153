from time import sleep

from models.connection import CreateConnection
from torch_sdk.models.profile import ProfilingType, JobType
from models.tags import ClassificationConfig
from torch_sdk.models.create_asset import AssetMetadata
from torch_client import TorchClient
from torch_sdk.models.datasource import CreateDataSource, SourceType, ConfigProperty

torch_client = TorchClient(url="https://torch.acceldata.local:5443",
                           access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")
from torch_airflow_sdk.decorators.span import span
from torch_airflow_sdk.operators.span_operator import SpanOperator


# get connection types
# connection_types = torch_client.get_connection_types()
# print(connection_types)

# get tags defined in torch, update protection flag, delete tag
# tags = torch_client.get_tags()
# print(tags)
# torch_client.update_data_protection(tag='asset_tag', is_protected=True)
# torch_client.delete_tag(tag='asset_tag')


# get related assets and child assets
# datasource = torch_client.get_datasource('postgres_ds_local')
# asset = datasource.get_asset(id=20)
# relations = asset.get_related_assets()
# print(relations)
# child_assets = asset.get_child_assets()
# print(child_assets)

# discover
# discover_res = torch_client.discover()
# print(discover_res)

# watch asset
# start_watch = asset.start_watch()
# print(start_watch)
# asset.stop_watch()

# tags
# tags = asset.get_asset_tags()
# print(tags)
# tag_add = asset.add_asset_tag(tag='asset_tag')
# print(tag_add)
# tag_rm = asset.remove_asset_tag(tag='asset_tag')
# print(tag_rm)


# asset activty
# activty = asset.get_asset_activity()
# print(activty)

# asset comment
# comments = asset.get_asset_comment()
# print(comments)

# labels
# labels = asset.add_asset_labels(labels = ['teamtorch', 'comp:adinc'])
# print(labels)
# labels = asset.get_asset_labels()
# print(labels)

# annotation
# annotation = asset.update_asset_annotation(annotation='this asset is created and accessed from torch sdk')
# print(annotation)

# delete an asset
# datasource.delete_asset(id=9523)

# list all snapshots
# snapshots = datasource.list_all_snapshots()
# print(snapshots)
# snapshots = torch_client.list_all_snapshots()
# print(snapshots)

# get user
# user = torch_client.get_user(user_id=3)
# print(user)
# user = torch_client.get_user(username='admin')
# print(user)

# crawler
# datasource.start_crawler()
# datasource.get_crawler_status()
# datasource.restart_crawler()

# api keys
# keys = torch_client.create_api_key()
# print(torch_client.get_api_keys())
# torch_client.delete_api_key(keys.accessKey)

# notifications
# print(torch_client.get_notifications())
# print(torch_client.get_incidents())

# analysis pipelines
# print(torch_client.get_analysis_pipeline(1))
# print(torch_client.list_all_analysis_pipelines())

# data sources : create, update, delete
# print(torch_client.get_all_datasources())

# datasource = CreateDataSource(
#     name='snowflake_ds_local',
#     sourceType=SourceType(5, 'SNOWFLAKE'),
#     description='snowflake schema',
#     connectionId=9,
#     configProperties=[ConfigProperty(key='jdbc.warehouse', value='COMPUTE_WH'),
#                       ConfigProperty(key='databases.0', value='FINANCE')]
# )
# ds_res = torch_client.create_datasource(datasource)
# ds_res = torch_client.get_datasource('snowflake_ds_local')

# datasource = CreateDataSource(
#     name='snowflake_ds_local',
#     sourceType=SourceType(5, 'SNOWFLAKE'),
#     description='snowflake schema',
#     connectionId=9,
#     configProperties=[ConfigProperty(key='jdbc.warehouse', value='COMPUTE_WH'),
#                       ConfigProperty(key='databases.0', value='CRAWLER_DB1')]
# )
# ds_res = ds_res.update_datasource(datasource)

# print(ds_res.get_root_assets())

# auto profile configs
# print(torch_client.get_all_auto_profile_configurations())
# ds_res = torch_client.get_datasource('postgres_ds_local')
# print(ds_res.get_auto_profile_configuration())
# ds_res.remove_auto_profile_configuration()

# asset metadata
# asset = torch_client.get_asset(id=1128)
# metadata = [AssetMetadata('STRING', 'key', 'source', 'value'), AssetMetadata('STRING', 's3_location', 'AWS_S3', 's3://aws/path/test/logs')]
# asset.update_asset_metadata(metadata)
# print(asset.get_asset_metadata())

# profile an asset, get profile req details, cancel profile, autotag profile
# asset = torch_client.get_asset(id=3)
# profile_res = asset.profile_asset(profiling_type= ProfilingType.SAMPLE, job_type=JobType.MINI_PROFILE)
# sleep(10)
# profile_req_details = profile_res.get_profile_request_details()
# cancel_profile_res = profile_res.cancel_profile()
# profile_res = asset.get_profile_status()
# autotag_res = asset.auto_tag_asset()
# profile_req_details_by_req_id = asset.get_profile_request_details(req_id= 845)

# sample data
# sample_data = asset.sample_data()

# classification configs : get all, create, update, delete
# configs = torch_client.list_all_classification_configurations()
# create_config = ClassificationConfig(
#     name='CCV',
#     protectedData=False,
#     classification='regex',
#     classificationType='card',
#     enabled= False,
#     description='Card CCV Checking with regex',
#     defaultValue='^\\d{3}$',
#     value='^\\d{4}$'
# )
# config_created = torch_client.create_classification_configuration(create_config)
# config = torch_client.get_classification_configuration(name='CCV')
# update_config = ClassificationConfig(
#     id=config.id,
#     name='CCV',
#     protectedData=False,
#     classification='regex',
#     classificationType='card',
#     enabled= False,
#     description='Card CCV Checking with regex',
#     defaultValue='^\\d{3}$',
#     value='^\\d{3}$'
# )
# config_updated = torch_client.update_classification_configuration(update_config)
# torch_client.delete_classification_configuration(name='CCV')


# setting groups
# setting_groups = torch_client.list_setting_groups()
# settings = torch_client.find_settings_by_group(setting_group_name= 'data_protection')
# setting = torch_client.get_setting(key='notification.channels.email.toEmail')
# updated_setting = torch_client.update_setting_value(key='data.protection.enabled', value="true")
# reset_setting_value = torch_client.reset_setting_value(key='data.protection.enabled')

# connections : create, update, check, list all
# connection_list = torch_client.list_all_connections()
# print(connection_list)
# torch_client.delete_connection(id=12)
# create_conn_obj = CreateConnection(
#     name='mysql_connection_sdk',
#     description='create connection from torch sdk',
#     connection_type_id=12,
#     analytics_pipeline_id=1,
#     properties=[ConfigProperty(key='jdbc.url', value='jdbc:postgresql://localhost:5432/'),
#                 ConfigProperty(key='jdbc.user', value='admin'),
#                 ConfigProperty(key='jdbc.password', value='admin')]
# )
# created_conn = torch_client.create_connection(create_conn_obj)
# update_conn_obj = CreateConnection(
#     name='mysql_connection_sdk',
#     description='create connection from torch sdk',
#     connection_type_id=12,
#     analytics_pipeline_id=1,
#     properties=[ConfigProperty(key='jdbc.url', value='jdbc:postgresql://localhost:5432/'),
#                 ConfigProperty(key='jdbc.user', value='admin'),
#                 ConfigProperty(key='jdbc.password', value='admin')]
# )
# updated_conn = torch_client.update_connection(update_connection=update_conn_obj)
# check_conn_status = torch_client.check_connection(update_conn_obj)
# get_conn = torch_client.get_connection(name='mysql_connection_sdk')


# rule execution and ops
# enable_rule = torch_client.enable_rule(rule_id=12)
# disable_rule = torch_client.disable_rule(rule_id=18)
# cancel_rule = torch_client.cancel_rule_execution(execution_id=1)
# execute_dq_rule = torch_client.execute_dq_rule(rule_id=18)
# execute_reconciliation_rule = torch_client.execute_reconciliation_rule(rule_id=24)
get_dq_execution_details = torch_client.get_dq_rule_execution_details(execution_id=62)
print(get_dq_execution_details.execution.executionStatus)
print(get_dq_execution_details.execution.resultStatus)

# get_recon_exe_details = torch_client.get_reconciliation_rule_execution_details(execution_id=64)
# print(get_recon_exe_details)