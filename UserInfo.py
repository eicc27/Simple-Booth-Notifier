class UserInfo:
    def __init__(self, name: str, goods: list[str], timeStr: str) -> None:
        self._name = name
        self._goods = goods
        self._timestamp = timeStr
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def goods(self) -> list[str]:
        return self._goods
    
    @goods.setter
    def goods(self, value: list[str]) -> None:
        self._goods = value

    @property
    def timestamp(self) -> str:
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, value: str) -> None:
        self._timestamp = value