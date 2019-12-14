class Log_Coupling:

    def __init__(self, event_entry):
        """
        Dictionary that labels things by their event_start time
        Therefore if it is within 10 minutes of that inital time
        bucket the event entry
        """
        self.event_times = {}
        self.origin_event = event_entry

    def add_entry(self, log_entry):
        # See if the log can be added to already made time bucket
        for time in self.event_times.keys():
            if(log_entry["EVENT_TIME"] - time <= 1800.0):
                return

        # Create new time bucket
        self.event_times[log_entry["EVENT_TIME"]] = log_entry
