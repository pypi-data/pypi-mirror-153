

class TimeoutFormatError(Exception):
    pass


class JobNotFound(Exception):
    def __init__(self, execid):
        msg = f"id {execid} not found"
        super().__init__(msg)

class JobDecodingError(Exception):
    def __init__(self, id):
        msg = f"error decoding {id}"
        super().__init__(msg)


class FunctionCallError(Exception):
    def __init__(self, func_name, error):
        msg = f"{func_name} failed with error: {error}"
        super().__init__(msg)
