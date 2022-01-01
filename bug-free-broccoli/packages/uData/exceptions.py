class TypeAndURLMatchException(Exception):
    def __init__(self, message=None):
        super().__init__(f'There was an error on crawler type and url: '
                         f'{message}')