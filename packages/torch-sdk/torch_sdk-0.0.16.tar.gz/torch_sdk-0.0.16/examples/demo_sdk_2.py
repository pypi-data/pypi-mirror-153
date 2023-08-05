from time import sleep

from models.connection import CreateConnection
from torch_sdk.models.profile import ProfilingType, JobType
from models.tags import ClassificationConfig
from torch_sdk.models.create_asset import AssetMetadata
from torch_client import TorchClient
from torch_sdk.models.datasource import CreateDataSource, SourceType, ConfigProperty, Crawler

torch_client = TorchClient(url="https://host5:5443",
                           access_key="185SF1I1G5LC", secret_key="vTGzcTbXYvIhbeKGj4Zsk3KNQPbQTK")

datasource_name = 'SNOWFLAKE_DATASOURCE_SDK'
datasource_details = torch_client.get_datasource(datasource_name)
asset_uid = datasource_name + ".CUSTOMERS_DATABASE.CUSTOMERS.CUSTOMERS"
asset = datasource_details.get_asset(uid=asset_uid)
print(asset)

asset.add_asset_labels(labels=['alias:customers sdk'])

asset.add_asset_tag('custom_sdk_tag')
asset.add_asset_tag('my_tag')
profile_res = asset.profile_asset(profiling_type=ProfilingType.FULL, job_type=JobType.PROFILE)
# asset.profile_asset(profiling_type= ProfilingType.SAMPLE, job_type=JobType.MINI_PROFILE)
# profile_status = dict(dict(profile_res.get_profile_request_details()).get('profileRequest')).get('status')
# print(profile_req_details)
# sleep(20)
# profile_req_details = dict(profile_res.get_profile_request_details()).get('status')
# print(profile_req_details)

profile_status = dict(dict(profile_res.get_profile_request_details()).get('profileRequest')).get('status')
while profile_status == 'IN PROGRESS':
    print('customer asset profiling in progress')
    sleep(3)
    profile_status = dict(dict(profile_res.get_profile_request_details()).get('profileRequest')).get('status')
profile_status = dict(dict(profile_res.get_profile_request_details()).get('profileRequest')).get('status')
print(profile_status)