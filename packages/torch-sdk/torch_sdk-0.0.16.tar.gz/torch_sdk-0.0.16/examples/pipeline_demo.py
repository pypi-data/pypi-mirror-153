import psycopg2
import random
import datetime
import time

from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_sdk.events.generic_event import GenericEvent
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from torch_sdk.torch_client import TorchClient


def create_torch_client():
    return TorchClient(url='https://acceldata.mars.acceldata.dev/torch', access_key = '8V4CBJZZL70QTC7', secret_key ='NM4L5ESV9F65SN5AP0C7L8UUAE1H01')


def create_pipeline(torch_client):
    pipeline = CreatePipeline(
        uid='customer.orders.monthly',
        name='Customer Orders Monthly aggregate',
        description='Pipeline to Aggregate the customer orders over 1 year',
        meta=PipelineMetadata(
            owner='vaishvik', team='torch_sdk_code', codeLocation='...'),
        context={'associated_tables': 'pipeline.customer, pipeline.orders, pipeline.customer_orders, pipeline.customer_orders_monthly_agg'}
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
            Dataset('snowflake1647503515210',
                    'FINANCE.FINANCE.A1'), Dataset('snowflake1647503515210',
                                                         'FINANCE.FINANCE.A2')],
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
        inputs=[Dataset('snowflake1647503515210',
                        'FINANCE.FINANCE.A1'), Dataset('snowflake1647503515210',
                                                             'FINANCE.FINANCE.A2')],
        outputs=[
            Dataset('snowflake1647503515210',
                    'FINANCE.FINANCE.A3')],
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
        description='Joins the ',
        inputs=[Dataset('snowflake1647503515210',
                        'FINANCE.FINANCE.A3')],
        outputs=[
            Dataset('snowflake1647503515210',
                    'FINANCE.FINANCE.A4')],
        meta=JobMetadata(owner='vaishvik', team='backend',
                         codeLocation='https://github.com/acme/reporting/reporting.scala'),
        context={}
    )
    job = pipeline.create_job(job)
    print('Created Job for monthly aggregation')
    return job


def create_conn():
    return None
    # return psycopg2.connect(
    #     host="torch.acceldata.local",
    #     port=5433,
    #     database="example",
    #     user="postgres",
    #     password="postgres")


def create_customer(index):
    return "customer" + str(index)


def create_orders(customer_id):
    orders = []
    for i in range(5):
        add_months = random.randint(0, 11)
        order = {
            'customer_id': customer_id,
            'items_count': random.randint(5, 10),
            'unit_price': random.randint(10, 20),
            'created_at': datetime.datetime(2021, 1, 1) +
            datetime.timedelta(days=30 * add_months)
        }
        orders.append(order)
    return orders


def insert_data(conn, span_context):
    customer_sql = """INSERT INTO pipeline.customers(name) VALUES(%s) RETURNING id;"""
    orders_sql = """INSERT INTO pipeline.orders(customer_id, items_count, unit_price, created_at) VALUES(%s, %s, %s, %s) RETURNING id;"""
    datagen_span_context = span_context.create_child_span(
        uid="customer.orders.datagen.span", context_data={'client_time': str(datetime.datetime.now())})
    customer_datagen_span = datagen_span_context.create_child_span(
        uid="customer.data.gen", context_data={'client_time': str(datetime.datetime.now())})

    # cur = conn.cursor()
    # customer_ids = []
    # print("Creating dummy customers")
    # for i in range(1, 101):
    #     customer_name = create_customer(i)
    #     cur.execute(customer_sql, (customer_name,))
    #     customer_id = cur.fetchone()[0]
    #     customer_ids.append(customer_id)
    # conn.commit()

    time.sleep(2)

    customer_datagen_span.end(
        {'client_time': str(datetime.datetime.now()), 'customers_count': 100})

    print("Creating dummy orders for each customers")
    orders_datagen_span = datagen_span_context.create_child_span(
        uid="order.data.gen", context_data={'client_time': str(datetime.datetime.now())})

    # cur = conn.cursor()
    # count = 0
    # for customer_id in customer_ids:
    #     customer_orders = create_orders(customer_id)
    #     for order in customer_orders:
    #         cur.execute(orders_sql, (customer_id,
    #                                  order['items_count'], order['unit_price'], order['created_at']))
    #         count += 1
    #
    # cur.close()
    # conn.commit()

    time.sleep(2)
    orders_datagen_span.end(
        {'client_time': str(datetime.datetime.now()), 'orders_count': 100})
    datagen_span_context.end({'client_time': str(datetime.datetime.now())})


def execute_join_orders_query(conn, span_context):
    join_sql = """SELECT co.id as customer_id, co.name, o.items_count * o.unit_price as total_order_value, o.created_at as ordered_at
    FROM pipeline.orders o JOIN pipeline.customers co on o.customer_id = co.id;"""

    join_span_context = span_context.create_child_span(
        uid="customer.orders.join.span", context_data={'client_time': str(datetime.datetime.now())})
    print("Joining customers and orders")
    # cur = conn.cursor()
    # cur.execute(join_sql)
    # rows = cur.fetchall()
    # cur.close()
    # conn.commit()
    # time.sleep(2)
    join_span_context.send_event(GenericEvent(context_data={'client_time': str(
        datetime.datetime.now()), 'row_count': 100}, event_uid="order.customer.join.result"))
    join_span_context.end(
        {'client_time': str(datetime.datetime.now()), 'row_count': 100})
    return None


def insert_orders(conn, rows, span_context):
    insert_sql = """INSERT INTO pipeline.customer_orders(customer_id, customer_name, total_order_value, ordered_at)
             VALUES(%s, %s, %s, %s) RETURNING id;"""
    print("Inserting joined record into the orders table")
    insert_span_context = span_context.create_child_span(
        uid="customer.orders.insert.span", context_data={'client_time': str(datetime.datetime.now())})
    # cur = conn.cursor()
    # for row in rows:
    #     cur.execute(insert_sql, (row[0], row[1], row[2], row[3]))
    # cur.close()
    # conn.commit()
    time.sleep(2)
    insert_span_context.end({'client_time': str(datetime.datetime.now())})


def insert_aggregate_data(conn, span_context):
    insert_sql = """
      INSERT INTO pipeline.customer_orders_monthly_agg(customer_name, customer_id, order_month, total_order_value)
      SELECT customer_name, customer_id,EXTRACT(MONTH FROM ordered_at) as month, SUM(total_order_value)
      FROM pipeline.customer_orders GROUP BY customer_name, EXTRACT(MONTH FROM ordered_at), customer_id;
    """
    print("Aggregating the orders over months per customer")
    agg_span_context = span_context.create_child_span(
        uid="monthy.aggregate.span", context_data={'client_time': str(datetime.datetime.now())})
    # cur = conn.cursor()
    # cur.execute(insert_sql)
    # cur.close()
    # conn.commit()
    time.sleep(2)
    agg_span_context.end({'client_time': str(datetime.datetime.now())})


if __name__ == "__main__":
    torch_client = create_torch_client()
    conn = create_conn()

    pipeline = create_pipeline(torch_client)
    pipeline_run = create_pipeline_run(pipeline)
    create_datagen_job(pipeline)
    create_data_join_job(pipeline)
    create_data_agg_job(pipeline)

    span_context = start_main_span(pipeline_run)
    insert_data(conn, span_context)
    time.sleep(2)
    rows = execute_join_orders_query(conn, span_context)
    time.sleep(2)
    insert_orders(conn, None, span_context)
    time.sleep(2)
    insert_aggregate_data(conn, span_context)
    time.sleep(2)
    # conn.close()
    end_main_span(span_context)
    end_pipeline_run(pipeline_run)
