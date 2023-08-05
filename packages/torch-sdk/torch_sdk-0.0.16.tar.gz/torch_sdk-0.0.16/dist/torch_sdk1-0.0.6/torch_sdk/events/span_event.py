from torch_sdk.models.span import CreateSpanEvent


class SpanEvent:
    """
        Description:
            Base class for all span event supported in torch
    """

    def event_uid_validation(self, event_uid: str):
        uid = event_uid.replace(" ", "")
        return uid.replace("_", ".")

    def convert(self, event_uid: str, span_id: int, context_data=None, log_data=None, client=None):
        """
        :param event_uid: event uid. similar to event type
        :param log_data: log data for the event
        :param context_data: context data map
        :param span_id: span id
        :param client: TorchClient class instance
        :return: SpanContextEvent class instance of the executed event
        """
        event_uid = self.event_uid_validation(event_uid)
        span_event = CreateSpanEvent(
            event_uid=event_uid,
            span_id=span_id,
            context_data=context_data,
            log_data=log_data
        )
        event_response = client.create_span_event(span_event)
        return event_response
