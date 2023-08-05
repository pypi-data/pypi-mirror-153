from time import sleep

from torch_sdk.models.connection import CreateConnection
from torch_sdk.models.profile import ProfilingType, JobType
from torch_sdk.torch_client import TorchClient
from torch_sdk.models.datasource import CreateDataSource, SourceType, ConfigProperty, Crawler

# initiate torch client using api keys
torch_client = TorchClient(url="https://host5:5443",
                           access_key="185SF1I1G5LC", secret_key="vTGzcTbXYvIhbeKGj4Zsk3KNQPbQTK")

# configurations static names
connection_type = 'SNOWFLAKE'
connection_name = 'snowflake_connection'
datasource_name = 'SNOWFLAKE_DATASOURCE_SDK'

snowflake_connection_type_id = None
source_type_id = None
customer_rule_id = 1004

# fetch source and connection type data
for source_type in torch_client.get_all_source_types():
    if source_type.name == connection_type:
        source_type_id = source_type.id
        snowflake_connection_type_id = source_type.connectionTypeId

# fetch analysis pipeline id
analytics_pipeline_id = None
for pipeline in torch_client.list_all_analysis_pipelines():
    if pipeline.name == 'Default':
        analytics_pipeline_id = pipeline.id

create_conn_obj = CreateConnection(
    name=connection_name,
    description='snowflake connection from sdk',
    connection_type_id=snowflake_connection_type_id,
    analytics_pipeline_id=analytics_pipeline_id,
    properties=[ConfigProperty(key='jdbc.url', value='jdbc:snowflake://kf71436.us-east-1.snowflakecomputing.com'),
                ConfigProperty(key='jdbc.user', value='winash'),
                ConfigProperty(key='jdbc.password', value='myD33ksh@k@n@lu')]
)

# test connection
check_conn_status = torch_client.check_connection(create_conn_obj)

if check_conn_status.status == 'SUCCESS':
    print('Snowflake test connection succeed')
    # create a connection
    connection_details = torch_client.create_connection(create_conn_obj)
    print('Snowflake connection created successfully.')
    datasource = CreateDataSource(
        name=datasource_name,
        sourceType=SourceType(source_type_id, connection_type),
        description='Datasource snowflake from sdk',
        connectionId=connection_details.id,
        configProperties=[ConfigProperty(key='jdbc.warehouse', value='COMPUTE_WH'),
                          ConfigProperty(key='databases.0', value='CUSTOMERS_DATABASE')]
    )
    datasource_details = torch_client.create_datasource(datasource)
    print('Snowflake datasource created successfully.')

    # start a crawler
    datasource_details.start_crawler()
    sleep(10)

    # get crawler status
    crawler_status: Crawler = datasource_details.get_crawler_status()
    while crawler_status.status == 'Running':
        print('Snowflake - Crawler running .....')
        sleep(30)
        crawler_status: Crawler = datasource_details.get_crawler_status()
    sleep(5)
    print('Crawling of snowflake datasource completed successfully.')

    # get an asset
    asset_uid = datasource_name + ".CUSTOMERS_DATABASE.CUSTOMERS.CUSTOMERS"
    asset = datasource_details.get_asset(uid=asset_uid)
    print('Updating customer asset details : tags, labels, annotation.')

    # add asset tags
    asset.add_asset_tag('SDK_CUSTOMER')
    asset.add_asset_tag('AD_CUSTOMERS')

    # add asset alias and annotation
    asset.add_asset_labels(labels=['alias:CUSTOMERS SDK', 'team:torch', 'owner:joe'])
    annotation = asset.update_asset_annotation(annotation='This is the customer asset contains details of the '
                                                          'acceldata customers.')
    # sample an asset
    sample_data = asset.sample_data()

    # profile an asset
    profile_res = asset.profile_asset(profiling_type=ProfilingType.FULL, job_type=JobType.PROFILE)
    profile_status = dict(dict(profile_res.get_profile_request_details()).get('profileRequest')).get('status')
    while profile_status == 'IN PROGRESS':
        print('Customer asset profiling in progress .....')
        sleep(3)
        profile_status = dict(dict(profile_res.get_profile_request_details()).get('profileRequest')).get('status')
    print('Customer asset profiling completed successfully.')

    # execute dq rule
    customer_dq_rule = torch_client.execute_dq_rule(rule_id=customer_rule_id)
    while 1:
        customer_dq_execution_details = torch_client.get_dq_rule_execution_details(execution_id=customer_dq_rule.id)
        print('Checking execution result of customer data quality rule .....')
        if customer_dq_execution_details.execution.executionStatus == 'SUCCESSFUL' and customer_dq_execution_details.execution.resultStatus == 'SUCCESSFUL':
            print('Data quality rule is completed successfully for customer table.')
            break
        elif customer_dq_execution_details.execution.executionStatus == 'RUNNING' and customer_dq_execution_details.execution.resultStatus == 'RUNNING':
            sleep(5)
            continue
        else:
            raise Exception(f'Data quality rule is failed for customer table.')
    customer_dq_execution_details = torch_client.get_dq_rule_execution_details(execution_id=customer_dq_rule.id)
    print('Customer DQ Rule Execution Details: ', customer_dq_execution_details.__dict__)


else:
    print('Snowflake test connection has been failed. Kindly verify credentials')
