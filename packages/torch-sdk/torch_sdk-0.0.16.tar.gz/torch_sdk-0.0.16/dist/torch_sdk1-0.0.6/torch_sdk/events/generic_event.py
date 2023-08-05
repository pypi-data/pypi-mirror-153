from torch_sdk.events.span_event import SpanEvent


class GenericEvent(SpanEvent):
    """
        Description:
            Class to send any custom event to Torch. `event_uid` should be set
            here and the context data.
    """

    def __init__(self, event_uid, context_data=None):
        self.context_data = context_data
        self.event_uid = event_uid
