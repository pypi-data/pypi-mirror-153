
class InvalidFrameworkException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        # self.args = f'The frame work should in one of these {args}'
