from models.span_context import SpanContext
from torch_client import TorchClient

from torch_airflow_sdk.decorators.span import span
from torch_airflow_sdk.operators.span_operator import SpanOperator

torch_client = TorchClient(url="https://torch.acceldata.local:5443",
                           access_key="N1LTYRK630PZ", secret_key="xPeUj4Iyj4WL2Tw284s9mqsgxvbPKW")
pipeline_uid = 'talend.etl.demo'

pipeline = torch_client.get_pipeline(pipeline_uid)


pipelineRunResponse = pipeline.create_pipeline_run(context_data={'team': 'torch_sdk_code', 'name': 'backend'})
spanContext = pipelineRunResponse.create_span(uid='parent_span',
                                              context_data={'start': 'tuesday', 'name': 'vaishvik'})

pipeline_run = pipeline.get_latest_pipeline_run()
span_context = pipeline_run.get_span(span_uid='parent_span')
print('done1')

parent_span_context = span_context
first_span_context = parent_span_context.create_child_span(uid='first_span',
                                                         context_data={'time': 'abcd'})

parent_span_context_dict = parent_span_context.__dict__
print('done2')
get_parent_span_context = SpanContext(**parent_span_context_dict)
second_span_context = get_parent_span_context.create_child_span(uid='second_span',
                                                         context_data={'time': 'def'})
