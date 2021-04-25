class AlreadyExistsError(Exception):
    pass

class ValidationError(Exception):
    pass

class DataFrameUnreadError(Exception):
    pass


class FetchFunctionUnresolvedError(Exception):
    pass


class ReadFunctionUnresolvedError(Exception):
    pass
