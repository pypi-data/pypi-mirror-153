import logging

from torch_sdk.initialiser import torch_client_credentials
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata
from torch_sdk.torch_client import TorchClient

logging.basicConfig(level=logging.INFO)

# Set up torch_sdk_code client
torch_client = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")
# create pipeline object
# pipeline = CreatePipeline(
#     uid='monthly_reporting-airflow_span_decorator',
#     name='Monthly reporting Pipeline-airflow span_decorator',
#     description='Pipeline to create monthly reporting tables',
#     meta=PipelineMetadata('Vaishvik', 'torch_sdk_code', '...'),
#     context={'key1': 'value1'}
# )
pipeline = CreatePipeline(
    uid='customer.orders.monthly.agg.demo',
    name='Customer Orders Monthly aggregate',
    description='Pipeline to Aggregate the customer orders over 1 year',
    meta=PipelineMetadata(
        owner='vaishvik', team='torch_sdk_code', codeLocation='...'),
    context={
        'associated_tables': 'pipeline.customer, pipeline.orders, pipeline.customer_orders, pipeline.customer_orders_monthly_agg'}
)
# creating pipeline using torch_sdk_code client
pipelineResponse = torch_client.create_pipeline(pipeline=pipeline)
print('Newly Created Pipeline Response : ', pipelineResponse)

# create a pipeline run of the pipeline
pipelineRunResponse = pipelineResponse.create_pipeline_run(context_data={'team': 'torch_sdk_code', 'name': 'backend'})
print('pipeline Run Created :', pipelineRunResponse)
#
# create span in the pipeline run
spanContext = pipelineRunResponse.create_span(uid='main_span',
                                              context_data={'start': 'tuesday', 'name': 'vaishvik'})
print('Span Created :', spanContext)

# check current span is root or not
print('span is root or not : ', spanContext.is_root())

# end the span event
print('Span End Event Response :', spanContext.end())

# check if the current span has children or not
print('has child ', spanContext.has_children())

# create a child span
childSpanContext = spanContext.create_child_span('span_uid_39_2')
print('child span is root or not  ', childSpanContext.is_root())
print('child span abort event : ', childSpanContext.abort())

print('child span has child or not : ', childSpanContext.has_children())
print('parent span has child or not : ', spanContext.has_children())
