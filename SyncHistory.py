import json

from UserInfo import UserInfo

class SyncHistory:
    """
        Initializes the history.
        
        ------
        
        parameters:

        `targetPath`: `str`, the path of the target file.

    """
    def __init__(self, targetPath="./history.json") -> None:
        self._targetPath = targetPath
        self._users = self._getHistoryInfo()

    def _getHistoryInfo(self) -> list[UserInfo]:
        """
        Gets the history info from the target file.
        
        The example format of history.json are as below.

        Examples
        ------
    
        {
        "users": {
        "amenochiyuki": {
            "goods": [
                "2664093", ...
            ],
            "timestamp": "2022-04-04 10:52:00"
                }, ...
            }
        }
        """
        file = json.load(open(self._targetPath, "r", encoding="utf-8"))
        fileUsers = file["users"]
        users = []
        for userName, userInfo in fileUsers.items():
            goods = userInfo["goods"]
            timestamp = userInfo["timestamp"]
            users.append(UserInfo(userName, goods, timestamp))
        return users

    def __getitem__(self, index: int):
        return self._users[index]
    
    def __setitem__(self, index: int, value: UserInfo):
        self._users[index] = value
    
    def writeBack(self):
        """
            Writes users back to history.json.
        """
        file = json.load(open(self._targetPath, "r", encoding="utf-8"))
        fileUsers = file["users"]
        for userInfo in self._users:
            userName = userInfo.userName
            fileUsers[userName] = {
                "goods": userInfo.goodIDs,
                "timestamp": userInfo.timestamp
            }
        json.dump(file, open(self._targetPath, "w", encoding="utf-8"), indent=4)
        

