import logging


class ExcludeEventsFilter(logging.Filter):
    def __init__(self, excluded_event_type=None):
        super().__init__()
        self.excluded_event_type = excluded_event_type

    def filter(self, record):
        if not isinstance(record.msg, dict) or self.excluded_event_type is None:
            return True  # Include the log message if msg is not a dictionary or excluded_event_type is not provided

        if record.msg.get("event") in self.excluded_event_type:
            return False  # Exclude the log message
        return True  # Include the log message
