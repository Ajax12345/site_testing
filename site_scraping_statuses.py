
class Status:
    def __init__(self, _name:str, _result:str, **kwargs) -> None:
        self.name, self.result = _name, _result
        self.__dict__.update(kwargs)

    

