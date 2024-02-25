class cooldown_error(Exception):
    def __init__(self, error_message: str, time_left: int):
        self.error_message = error_message
        self.time_left = time_left