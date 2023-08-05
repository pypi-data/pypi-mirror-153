import logging

from torch_sdk.initialiser import torch_client_credentials
from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from torch_sdk.torch_client import TorchClient

logging.basicConfig(level=logging.INFO)

# Set up torch_sdk_code client
torchClient = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")

# create pipeline object
pipeline = CreatePipeline(
    uid='monthly_reporting_airflow_2',
    name='Monthly reporting Pipeline_airflow_2',
    description='Pipeline to create monthly reporting tables',
    meta=PipelineMetadata('vaishvik', 'torch_sdk_code', '...'),
    context={'key1': 'value1'}
)
# creating pipeline using torch_sdk_code client
pipelineResponse = torchClient.create_pipeline(pipeline=pipeline)
print('Newly Created Pipeline Response : ', pipelineResponse)

# create job object
job = CreateJob(
    uid='monthly_sales_aggregate-38',
    name='Monthly Sales Aggregate-38',
    pipelineSnapshot=pipeline.currentSnapshot,
    description='Generates the monthly sales aggregate tables for the complete year',
    inputs=[Dataset('postgres-assembly-5450', 'ad_catalog.ad_catalog.flyway_schema_history')],
    outputs=[Dataset('postgres-ds', 'ad_catalog.ad_catalog.flyway_schema_history')],
    meta=JobMetadata('vaishvik', 'backend', 'https://github.com/acme/reporting/reporting.scala'),
    context={'key21': 'value21'}
)
# create a job on newly created pipeline
jobResponse = pipelineResponse.create_job(job)
print('Newly Created Job Response : ', jobResponse)

# create a pipeline run of the pipeline
pipelineRunResponse = pipelineResponse.create_pipeline_run()
print('pipeline Run Created :', pipelineRunResponse)

# update a pipeline run of the pipeline
updatePipelineRunRes = pipelineRunResponse.update_pipeline_run(context_data={'key1': 'value2', 'name': 'backend'},
                                                               result=PipelineRunResult.SUCCESS,
                                                               status=PipelineRunStatus.COMPLETED)
print('pipeline run updated :', updatePipelineRunRes)

# create span in the pipeline run
spanContext = pipelineRunResponse.create_span(uid='span_uid_38')
print('Span Created :', spanContext)

# # start span event
# print('Span Start Event Response :', spanContext.start({'k': 'v'}))

# check current span is root or not
print('span is root or not : ', spanContext.is_root())

# get span
sc = pipelineRunResponse.get_span(span_uid='span_uid_38')
print('span con get : ', sc)

sc2 = pipelineRunResponse.get_span(span_uid='span_uid_38')
print('span con get : ', sc2)

# end the span event
print('Span End Event Response :', spanContext.end())

# check if the current span has children or not
print('has child ', spanContext.has_children())

# # create a child span
# childSpanContext = spanContext.create_child_span('span_uid_38_2')
# print('child span is root or not  ', childSpanContext.is_root())
# print('child span abort event : ', childSpanContext.abort())
#
# print('child span has child or not : ', childSpanContext.has_children())
# print('parent span has child or not : ', spanContext.has_children())