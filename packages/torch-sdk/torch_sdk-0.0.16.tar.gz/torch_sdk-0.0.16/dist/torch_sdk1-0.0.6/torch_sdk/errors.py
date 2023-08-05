class TorchError(Exception):
    pass


class APIError(TorchError):
    pass

class TorchSdkException(Exception):
    pass