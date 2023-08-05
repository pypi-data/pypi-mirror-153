from torch_sdk.events.span_event import SpanEvent


class LogEvent(SpanEvent):
    """
        Description:
            Class to send log event to torch.
    """
    def __init__(self, log_data: str, context_data=None):
        """
        :param log_data: log data of the log event
        :param context_data: context data of event
        """
        self.log_data = log_data
        self.context_data = context_data
        self.event_uid = 'LOG'
