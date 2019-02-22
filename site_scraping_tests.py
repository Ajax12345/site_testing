import typing, datetime, os
import functools

def initialize(_f:typing.Callable) -> typing.Callable:
    @functools.wraps(_f)
    def _wrapper(_self, _payload:dict) -> typing.Any:
        with open(f'test_logger{sum(i.startswith("test_logger") for i in os.listdir(os.getcwd()))+1}.txt', 'a') as f:
            d = datetime.datetime.now()
            f.write(f"{str(d)}: Intializing test => name={_payload['name']}, email={_payload['email']}\n")

        return _f(_self, _payload)
    return _wrapper

def task(_f:typing.Callable) -> typing.Callable:
    def _wrapper(_self, _payload:dict) -> None:
        _status = _f(_self, _payload)
        with open(f'test_logger{sum(i.startswith("test_logger") for i in os.listdir(os.getcwd()))}.txt', 'a') as f:
            d = datetime.datetime.now()
            f.write(f"{str(d)}: executed '{_f.__name__}'. Result: {['failed', 'succeeded'][_status.result]}\n")

        return _status
    return _wrapper