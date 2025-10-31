#!/usr/bin/env python3

class BaseError(Exception):
    def __init__(self, message = None):
        super().__init__(self, message)
        self.message = message


class ResultPropertyValueError(BaseError):
    def __init__(self, message=None, result=None):
        super().__init__(message)
        self.result = result

    def __str__(self):
        result = self.result
        return (
            f'{self.message}: type={result.type} name={result.name!r}'
            f' value={result.value!r} comment={result.comment!r}'
        )


class V:
    type = 123
    name = 'Name'
    value = None
    comment = None


v = V()
raise ResultPropertyValueError('Failed!', v)
