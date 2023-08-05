import logging

from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from torch_sdk.torch_client import TorchClient

logging.basicConfig(level=logging.INFO)

# Set up torch_sdk_code client
torchClient = TorchClient(url="https://torch.acceldata.local:5443/torch",
                          access_key="SY1Q793UECO38GB", secret_key="JQ9CUKVZKD8JBDNHMLFMDW5E3VCF8U")

# create pipeline object
pipeline = CreatePipeline(
    uid='TEST_PIPELINE',
    name='test pipeline',
    description='Pipeline for testing',
    meta=PipelineMetadata('Vaishvik', 'torch_sdk_code', '...'),
    context={'Key': 'value'}
)
# creating pipeline using torch_sdk_code client
pipelineResponse = torchClient.create_pipeline(pipeline=pipeline)
print('Newly Created Pipeline Response : ', pipelineResponse)

# create job object
job = CreateJob(
    uid='JOB_1',
    name='MIGRATION JOB',
    pipelineSnapshot=pipeline.currentSnapshot,
    description='migration job',
    inputs=[Dataset('pg_ds', 'ad_catalog.ad_catalog.flyway_schema_history')],
    outputs=[Dataset('pg_ds_new', 'ad_catalog.ad_catalog.flyway_schema_history')],
    meta=JobMetadata('vaishvik', 'backend', 'https://github.com/acme/reporting/reporting.scala'),
    context={'key21': 'value21'}
)
# create a job on newly created pipeline
jobResponse = pipelineResponse.create_job(job)
print('Newly Created Job Response : ', jobResponse)

# create a pipeline run of the pipeline
pipelineRunResponse = pipelineResponse.create_pipeline_run()
print('pipeline Run Created :', pipelineRunResponse)

# create span in the pipeline run
spanContext = pipelineRunResponse.create_span(uid='span_uid_38')
print('Span Created :', spanContext)

# check current span is root or not
print('span is root or not : ', spanContext.is_root())

# get span
sc = pipelineRunResponse.get_span(span_uid='span_uid_38')
print('span con get : ', sc)

# end the span event
print('Span End Event Response :', spanContext.end())

# check if the current span has children or not
print('has child ', spanContext.has_children())

# # create a child span
childSpanContext = spanContext.create_child_span('span_uid_38_2')
print('child span abort event : ', childSpanContext.abort())

childSpans = spanContext.get_child_spans()
print('child spans list: ', childSpans, ' ; size : ', len(childSpans))
print('has child ', spanContext.has_children())

# update a pipeline run of the pipeline
updatePipelineRunRes = pipelineRunResponse.update_pipeline_run(context_data={'key1': 'value2', 'name': 'backend'},
                                                               result=PipelineRunResult.SUCCESS,
                                                               status=PipelineRunStatus.COMPLETED)
print('pipeline run updated :', updatePipelineRunRes)
