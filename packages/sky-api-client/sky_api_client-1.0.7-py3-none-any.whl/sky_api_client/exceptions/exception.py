class GeneralError(Exception):
    pass


class MethodNotDefined(Exception):
    def __init__(self, method: str) -> None:
        self.method = method
        super().__init__('{} method is not available for this entity'.format(self.method))


class InvalidArguments(Exception):
    def __init__(self) -> None:
        super().__init__('Invalid Arguments')
