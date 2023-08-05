from dataclasses import dataclass
from enum import Enum


@dataclass
class SpanMetadata:
    owner: str = None


class SpanStatus(Enum):
    INITIALIZED = 1
    STARTED = 2
    FINISHED = 3
    ABORTED = 4
    FAILED = 5


class Span:

    def __init__(self, uid, pipelineRunId, status=SpanStatus.INITIALIZED, parentSpanId=None, id=None, startedAt=None,
                 finishedAt=None, **kwrgs):
        self.uid = uid
        self.pipelineRunId = pipelineRunId
        self.status = status
        if parentSpanId is not None:
            self.parentSpanId = parentSpanId
        if id is not None:
            self.id = id
            self.startedAt = startedAt
            self.finishedAt = finishedAt

    def __eq__(self, other):
        return self.uid == other.uid

    def __repr__(self):
        return f"Span({self.__dict__!r})"


class SpanEventType(Enum):
    SPAN_START = 'SPAN.START'
    SPAN_END = 'SPAN.END'
    SPAN_ABORTED = 'SPAN.ABORTED'
    SPAN_FAILED = 'SPAN.FAILED'


class SpanContextEvent:

    def __init__(self, eventUid: SpanEventType, spanId: int, contextData=None, id=None, **kwargs):
        """
            Description:
                span context event
        :param eventUid: event type
        :param spanId: span id
        :param contextData: context data of the event
        :param id: id of the event
        """
        self.eventUid = eventUid
        self.spanId = spanId
        self.contextData = contextData
        if id is not None:
            self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"SpanContextEvent({self.__dict__!r})"


class CreateSpanEvent:

    def __init__(self, event_uid: str, span_id: int, context_data: dict = None, log_data: str = None):
        """
            Description:
                Class used to create event for the span
            :param event_uid:
            :param span_id:
            :param context_data:
            :param log_data
        """
        self.eventUid = event_uid
        self.contextData = context_data
        self.logData = log_data
        self.spanId = span_id

    def __repr__(self):
        return f"CreateSpanEvent({self.__dict__!r})"
