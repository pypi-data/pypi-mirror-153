import logging

from torch_sdk.initialiser import torch_client_credentials
from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from torch_sdk.torch_client import TorchClient

logging.basicConfig(level=logging.INFO)

# Set up torch_sdk_code client
torchClient = TorchClient(url="https://torch.acceldata.local:5443",
                       access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")

# get pipeline object
pipeline = torchClient.get_pipeline('customer.orders.monthly.agg.demo')
print('pipeline response : ', pipeline)

# # create job object
job = CreateJob(
    uid='monthly_sales_aggregate-39',
    name='Monthly Sales Aggregate-39',
    pipelineSnapshot=pipeline.currentSnapshot,
    description='Generates the monthly sales aggregate tables for the complete year',
    inputs=[Dataset('postgres-assembly-5450', 'ad_catalog.ad_catalog.flyway_schema_history')],
    outputs=[Dataset('postgres-ds', 'ad_catalog.ad_catalog.flyway_schema_history')],
    meta=JobMetadata('Vaishvik_brahmbhatt', 'backend', 'https://github.com/acme/reporting/report.scala'),
    context={'job_time': 'weekend'}
)
# create a job on newly created pipeline
jobResponse = pipeline.create_job(job)
print('Newly Created Job Response : ', jobResponse)

# get latest pipeline run
pipeline_run = pipeline.get_latest_pipeline_run()
print('latest pipeline run : ', pipeline_run)

# create span in the pipeline run
span_context = pipeline_run.get_span(span_uid='main_span')
print('Span get :', span_context)

# end the span event
print('Span End Event Response :', span_context.end())

# check if the current span has children or not
print('has child ', span_context.has_children())

# # create a child span
# print('Created child span .........................')
#
# childSpanContext = span_context.create_child_span(uid='span_uid_39_3', context_data={'span': 'child', 'end': 'wednesday'})
# print('child span is root or not  ', childSpanContext.is_root())
# print('child span abort event : ', childSpanContext.abort())
# print('child span abort event : ', childSpanContext.abort())
# print('child span has child or not : ', childSpanContext.has_children())
#
# # update a pipeline run of the pipeline
# update_pipeline_run = pipeline_run.update_pipeline_run(context_data={'key1': 'value2', 'name': 'backend'},
#                                                        result=PipelineRunResult.SUCCESS,
#                                                        status=PipelineRunStatus.COMPLETED)
# print('pipeline run updated :', update_pipeline_run)
