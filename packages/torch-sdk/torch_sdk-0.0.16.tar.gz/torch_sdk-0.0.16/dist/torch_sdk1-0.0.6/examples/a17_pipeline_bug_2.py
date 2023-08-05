import datetime
import time

from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from torch_sdk.torch_client import TorchClient

def create_torch_client():
    # return TorchClient(
    #     url='https://acceldata.sso-demo.acceldata.dev/torch',
    #     access_key='1CXZ7RD61X1Z92F',
    #     secret_key='CKO7QJ2FZL7J12RIE06KUVRZSA2JOY'
    # )
    return TorchClient(
        url='https://a17bffb92ed5743d88e89cbfdd6a9c0c-1802836320.us-east-2.elb.amazonaws.com',
        access_key = '7GIF9LFARFX8',
        secret_key ='11ysBWOKU1t4eijydcldbd9kKiQcHV'
    )

def create_pipeline(torch_client):
    pipeline = CreatePipeline(
        # uid='pipeline.demo.first',
        # name='ETL PIPELINE - SDK ',
        uid='pipeline.demo.third',
        name='ETL PIPELINE - SDK - TORCH',
        description='Pipeline to Aggregate the customer orders over 1 year',
        meta=PipelineMetadata(
            owner='vaishvik', team='TORCH', codeLocation='www.v.co.in'),
        context={'tables': 'XYZ'}
    )
    pipeline_response = torch_client.create_pipeline(pipeline=pipeline)
    print('Created the pipeline')
    return pipeline_response


def create_datagen_job(pipeline):
    job = CreateJob(
        uid='datagen.job.1',
        name='DATAGEN JOB',
        pipelineSnapshot=pipeline.currentSnapshot,
        description='data gen job',
        inputs=[Dataset('AWS-S3-DS', 'airflow_order_details')],
        outputs=[
            Dataset('GCS-DS', 'customers')],
        meta=JobMetadata(owner='vaishvik', team='backend',
                         codeLocation='https://github.com/acme/reporting/reporting.scala'),
        context={}
    )
    job = pipeline.create_job(job)
    print('Created Job for random data insertion')
    return job


def create_insert_data_job(pipeline):
    job = CreateJob(
        uid='insert.data.job.2',
        name='INSERT DATA JOB',
        pipelineSnapshot=pipeline.currentSnapshot,
        description='insert data job',
        inputs=[Dataset('GCS-DS', 'customers')],
        outputs=[
            Dataset('AWS-RDS-DS', 'customers.public.products')],
        meta=JobMetadata(owner='vaishvik', team='backend',
                         codeLocation='https://github.com/acme/reporting/reporting.scala'),
        context={}
    )
    job = pipeline.create_job(job)
    print('Insert data Job for random data insertion')
    return job


def create_pipeline_run(pipeline):
    return pipeline.create_pipeline_run(
        context_data={'client_time': str(datetime.datetime.now())})


def start_main_span(pipeline_run):
    span_context = pipeline_run.create_span(
        uid='customer.orders.monthly.agg', context_data={'client_time': str(datetime.datetime.now())})
    return span_context


def end_main_span(span_context):
    span_context.end()


def end_pipeline_run(pipeline_run, result=PipelineRunResult.SUCCESS, status=PipelineRunStatus.COMPLETED):
    pipeline_run.update_pipeline_run(context_data={'client_time': str(datetime.datetime.now())},
                                     result=result,
                                     status=status)


if __name__ == "__main__":
    torch_client = create_torch_client()

    pipeline = create_pipeline(torch_client)
    pipeline_run = create_pipeline_run(pipeline)
    create_datagen_job(pipeline)
    create_insert_data_job(pipeline)
    span_context = start_main_span(pipeline_run)
    time.sleep(2)
    end_main_span(span_context)
    end_pipeline_run(pipeline_run)
