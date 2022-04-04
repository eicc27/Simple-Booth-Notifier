class UserInfo:
    def __init__(self, userName: str, goodIDs: list[str], timeStr: str) -> None:
        self._userName = userName
        self._goodIDs = goodIDs
        self._timestamp = timeStr
    
    @property
    def userName(self) -> str:
        return self._userName
    
    @property
    def goodIDs(self) -> list[str]:
        return self._goodIDs
    
    @goodIDs.setter
    def goodIDs(self, value: list[str]) -> None:
        self._goodIDs = value

    @property
    def timestamp(self) -> str:
        return self._timestamp
    
    @timestamp.setter
    def timestamp(self, value: str) -> None:
        self._timestamp = value