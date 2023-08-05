# Pipeline APIs
Acceldata Torch is a complete solution to observe the quality of the data present in your data lake and warehouse. Using Torch, you can ensure that high-quality data backs your business decisions. Torch provides you with tools to measure the quality of data in a data catalog and to never miss significant data sources. All users including analysts, data scientists, and developers, can rely on Torch to observe the data flowing in the warehouse or data lake and can rest assured that there is no loss of data. 
<br />
Torch SDK is used to trigger torch catalog and pipeline APIs. By creating a Torch client, all the torch apis can be accessed. 

Install `torch-sdk` pypi package in a python environment.
```bash
pip install torch-sdk
```

Read more about torch-sdk from [here](https://pypi.org/project/torch-airflow-sdk/)

## Create Torch Client
Torch client is used to send data to the torch servers. It consists of various methods to communicate with the torch server. Torch client have access to catalog and pipeline APIs. To create a torch client, torch url and API keys are required. To create torch API keys, go to torch ui’s settings and generate keys for the client.
```python
from torch_sdk.torch_client import TorchClient

torch_client = TorchClient(url='https://acceldata.host.dev:9999', access_key='******',
                         secret_key='*****************')

```

## Pipeline API 
There are various pipeline APIs are supported through torch sdk. Pipeline APIs like create pipeline, add jobs and spans, initiate pipeline run et cetera. Torch sdk is able to send various event during span life cycle. Hence, torch sdk has full control over the pipelines.
##### Create Pipeline And Job
Pipeline represents the ETL pipeline in its entirety and will contain Asset nodes and Jobs associated. The complete pipeline definition forms the Lineage graph for all the data assets.
</br>
Job Node or Process Node represents an entity that does some job in the ETL workflow. From this representation, Job’s input is some assets, and output is few other assets.
Torch will use the set of Jobs definition in the workflow to create the Lineage, and the will also track version changes for the Pipeline.

To create pipeline and jobs, first create creation object with required parameter. And with use of supported methods by sdk, can do corresponding operation on torch server side. 
```python
from torch_sdk.models.job import CreateJob, JobMetadata, Dataset
from torch_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus

# Create pipeline
pipeline = CreatePipeline(
    uid='monthly_reporting_pipeline',
    name='Monthly reporting Pipeline',
    description='Pipeline to create monthly reporting tables',
    meta=PipelineMetadata('Vaishvik', 'torch_sdk_code', '...'),
    context={'key1': 'value1'}
)
pipeline_response = torch_client.create_pipeline(pipeline=pipeline)

# Create Job
job = CreateJob(
    uid='monthly_sales_aggregate',
    name='Monthly Sales Aggregate',
    pipelineSnapshot=pipeline_response.currentSnapshot,
    description='Generates the monthly sales aggregate tables for the complete year',
    inputs=[Dataset('datasource-name', 'database.schema.table_1')],
    outputs=[Dataset('datasource-name', 'database.schema.table_2')],
    meta=JobMetadata('vaishvik', 'backend', 'https://github.com/'),
    context={'key21': 'value21'}
)
job_response = pipeline_response.create_job(job)
```
##### Create Pipeline Run And Generate Spans And Send Span Events

Pipeline run indicates the execution of the pipeline. The same pipeline can be executed multiple times and each execution (run) has new snapshot version. Each pipeline run has hierarchical span's group. A Span is a way to group a bunch of metrics, and they are hierarchical. It can be as granular as possible. The APIs will support creating a span object from a pipeline object, and then hierarchical spans are started from parent spans. A Span typically encompasses a process or a task and can be granular. This hierarchical system is powerful enough to model extremely complex pipeline observability flows. Optionally, a span can also be associated with a Job. This way, we can track starting and completion of Job, including the failure tracking. Start and stop are implicitly tracked for a span.

Torch sdk has also support for create new pipeline run, add spans in it. During the span life cycle, sdk is able to send some customs and standard span events to collect pipeline run metrics for observability.  
```python

from torch_sdk.events.generic_event import GenericEvent
from datetime import datetime

# create a pipeline run of the pipeline
pipeline_run = pipeline_response.create_pipeline_run()

# create span in the pipeline run
span_context = pipeline_run.create_span(uid='monthly.generate.data.span')

# check current span is root or not
span_context.is_root()

# end the span 
span_context.end()

# check if the current span has children or not
span_context.has_children()

# create a child span
child_span_context = span_context.create_child_span('monthly.generate.customer.span')

# send custom event
child_span_context.send_event(
    GenericEvent(context_data={'client_time': str(datetime.now()), 'row_count': 100}, 
                 event_uid="order.customer.join.result")
)


# abort span
child_span_context.abort()

# failed span
child_span_context.failed()

# update a pipeline run of the pipeline
updatePipelineRunRes = pipeline_run.update_pipeline_run(context_data={'key1': 'value2', 'name': 'backend'},
                                                               result=PipelineRunResult.SUCCESS,
                                                               status=PipelineRunStatus.COMPLETED)

```

##### Get Latest Pipeline Run
Torch sdk can get the latest pipeline run of the pipeline. with use of the latest pipeline run instance, user can continue ETL pipeline and add spans, jobs, events too. Hence, torch sdk has complete access on the torch pipeline service.
```python
pipeline = torch_client.get_pipeline('monthly.reporting.pipeline')

```
