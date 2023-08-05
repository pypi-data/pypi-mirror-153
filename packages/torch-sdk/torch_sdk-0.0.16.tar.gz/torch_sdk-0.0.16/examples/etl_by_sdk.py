import psycopg2
import random
import datetime
import time

from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_sdk.events.generic_event import GenericEvent
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from torch_sdk.torch_client import TorchClient

# data_source_name = 'postgres_ds_local'
# asset_1 = 'ad_catalog.ad_catalog.flyway_schema_history'
# asset_2 = 'ad_catalog.ad_catalog.source_models'
# asset_3 = 'ad_catalog.ad_catalog.source_types'
# asset_4 = 'ad_catalog.ad_catalog.assets'

# data_source_name = 'SNOWFLAKE_DS_PUBLIC'
# asset_1 = 'FINANCE.FINANCE.A1'
# asset_2 = 'FINANCE.FINANCE.A2'
# asset_3 = 'FINANCE.FINANCE.A3'
# asset_4 = 'FINANCE.FINANCE.A4'

data_source_name = 'REDSHIFT_DS'
asset_1 = 'dev.customers.test'
asset_2 = 'dev.customers.test2'
asset_3 = 'dev.customers.contacts'
asset_4 = 'dev.customers.datatypes'

def create_torch_client():
    # return TorchClient(
    #     url='https://neptune.demo.acceldata.dev/torch',
    #     access_key='VK8ZHTKZOMK2WH4',
    #     secret_key='G0HQVA47GOBWJ16RHLFU0D5V82AC2F')

    return TorchClient(
        url='https://winterfell.demo.acceldata.dev/torch',
        access_key='OG1YBHVDB84H11L',
        secret_key='EP4D1D2DKZSXXHCZLY5Z2YVQKA81FB')

    # return TorchClient(
    #     url='https://acceldata.acceldata.local:5443/torch',
    #     access_key='XO3JFEI02G93XS0',
    #     secret_key='1HFHZ9JMQQCHBD9DS3742B7TMDA0S8')
    #
    # return TorchClient(
    #     url='https://pepsi.acceldata.local:5443/torch',
    #     access_key='K9ZMZH2HBF8DZYV',
    #     secret_key='RITCFPMGU0AO2REZP05PRCF0RQBPQF')


def create_pipeline(torch_client):
    pipeline = CreatePipeline(
        uid='sso.multitenancy.etl.testing',
        name='SSO Multi tenancy testing - acceldata',
        description='Pipeline to Aggregate the customer orders over 1 year',
        meta=PipelineMetadata(
            owner='vaishvik', team='torch_sdk_code', codeLocation='...'),
        context={
            'associated_tables': 'pipeline.customer, pipeline.orders, pipeline.customer_orders, '
                                 'pipeline.customer_orders_monthly_agg'}
    )
    pipeline_response = torch_client.create_pipeline(pipeline=pipeline)
    print('Created the pipeline')
    return pipeline_response


def create_datagen_job(pipeline):
    job = CreateJob(
        uid='customer.order.datagen.job',
        name='customers and orders datagen',
        pipelineSnapshot=pipeline.currentSnapshot,
        description='Generates Pseudo random data for Orders and Customers',
        inputs=[],
        outputs=[
            Dataset(data_source_name,
                    asset_1), Dataset(data_source_name,
                                      asset_2)],
        meta=JobMetadata(owner='vaishvik', team='backend',
                         codeLocation='https://github.com/acme/reporting/reporting.scala'),
        context={}
    )
    job = pipeline.create_job(job)
    print('Created Job for random data insertion')
    return job


def create_data_join_job(pipeline):
    job = CreateJob(
        uid='customer.order.join.job',
        name='customers and orders joiner and Inserter',
        pipelineSnapshot=pipeline.currentSnapshot,
        description='Joins the ',
        inputs=[Dataset(data_source_name, asset_1), Dataset(data_source_name, asset_2)],
        outputs=[
            Dataset(data_source_name,
                    asset_3)],
        meta=JobMetadata(owner='vaishvik', team='backend',
                         codeLocation='https://github.com/acme/reporting/reporting.scala'),
        context={}
    )
    job = pipeline.create_job(job)
    print('Created Job for joined data read and insert')
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


def create_data_agg_job(pipeline):
    job = CreateJob(
        uid='monthly.order.aggregate.job',
        name='Aggregates the monthly orders',
        pipelineSnapshot=pipeline.currentSnapshot,
        description='Joins the ',
        inputs=[Dataset(data_source_name,
                        asset_3)],
        outputs=[
            Dataset(data_source_name,
                    asset_4)],
        meta=JobMetadata(owner='vaishvik', team='backend',
                         codeLocation='https://github.com/acme/reporting/reporting.scala'),
        context={}
    )
    job = pipeline.create_job(job)
    print('Created Job for monthly aggregation')
    return job


def insert_data(span_context):
    datagen_span_context = span_context.create_child_span(
        uid="customer.orders.datagen.span", context_data={'client_time': str(datetime.datetime.now())})
    customer_datagen_span = datagen_span_context.create_child_span(
        uid="customer.data.gen", context_data={'client_time': str(datetime.datetime.now())})

    time.sleep(2)
    customer_datagen_span.send_event(GenericEvent(context_data={'client_time': str(
        datetime.datetime.now()), 'customers_count': 100}, event_uid="customer.insert.data.result"))
    customer_datagen_span.end(
        {'client_time': str(datetime.datetime.now()), 'customers_count': 100})

    print("Creating dummy orders for each customers")
    orders_datagen_span = datagen_span_context.create_child_span(
        uid="order.data.gen", context_data={'client_time': str(datetime.datetime.now())})

    time.sleep(2)
    orders_datagen_span.send_event(GenericEvent(context_data={'client_time': str(
        datetime.datetime.now()), 'orders_count': 100}, event_uid="order.insert.data.result"))
    orders_datagen_span.end(
        {'client_time': str(datetime.datetime.now()), 'orders_count': 100})
    datagen_span_context.end({'client_time': str(datetime.datetime.now())})


def execute_join_orders_query(span_context):
    join_span_context = span_context.create_child_span(
        uid="customer.orders.join.span", context_data={'client_time': str(datetime.datetime.now())})
    print("Joining customers and orders")

    time.sleep(2)
    join_span_context.send_event(GenericEvent(context_data={'client_time': str(
        datetime.datetime.now()), 'row_count': 100}, event_uid="order.customer.join.result"))
    join_span_context.end(
        {'client_time': str(datetime.datetime.now()), 'row_count': 100})


def insert_orders(span_context):
    print("Inserting joined record into the orders table")
    insert_span_context = span_context.create_child_span(
        uid="customer.orders.insert.span", context_data={'client_time': str(datetime.datetime.now())})
    time.sleep(2)
    insert_span_context.send_event(GenericEvent(context_data={'client_time': str(
        datetime.datetime.now()), 'order_placed': 42}, event_uid="orders.placed.insert.data.result"))
    insert_span_context.end({'client_time': str(datetime.datetime.now())})


def insert_aggregate_data(span_context):
    print("Aggregating the orders over months per customer")
    agg_span_context = span_context.create_child_span(
        uid="monthy.aggregate.span", context_data={'client_time': str(datetime.datetime.now())})
    time.sleep(2)
    agg_span_context.send_event(GenericEvent(context_data={'client_time': str(
        datetime.datetime.now()), 'agg_data_counts': 62}, event_uid="monthly.aggregate.result"))
    agg_span_context.end({'client_time': str(datetime.datetime.now())})


if __name__ == "__main__":
    torch_client = create_torch_client()

    pipeline = create_pipeline(torch_client)
    pipeline_run = create_pipeline_run(pipeline)
    create_datagen_job(pipeline)
    create_data_join_job(pipeline)
    create_data_agg_job(pipeline)

    span_context = start_main_span(pipeline_run)
    insert_data(span_context)
    time.sleep(2)
    execute_join_orders_query(span_context)
    time.sleep(2)
    insert_orders(span_context)
    time.sleep(2)
    insert_aggregate_data(span_context)
    time.sleep(2)
    end_main_span(span_context)
    end_pipeline_run(pipeline_run)
