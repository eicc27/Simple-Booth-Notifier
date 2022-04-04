from datetime import datetime
from urllib import request as req
from lxml import etree
from fake_useragent import UserAgent
from UserInfo import UserInfo

class BoothCrawler:
    """
    Given a URL pointing to a user, and a synchronization history with a timestamp,
    the class tries to update that local history.
    
    ------

    parameters: 
    
    `userInfo`: `UserInfo`: the user info to be updated
    """

    PRODUCT_XPATH = "//li/@data-product-id"

    def __init__(self, userInfo: UserInfo) -> None:
        self._userInfo = userInfo
    
    @property
    def userInfo(self) -> UserInfo:
        return self._userInfo

    @staticmethod
    def _installFakeHeaderOpener():
        opener = req.build_opener()
        ua = UserAgent(path="./fakeua-0.11.1.json")
        opener.addheaders = [("User-Agent", ua.random)]
        req.install_opener(opener)

    def _getWebsiteInfo(self) -> list[str]:
        """
            Reaches the target website to get the goods list.
        
        ------

        returns:

        `list[str]`: the list of goods
        """
        userName = self._userInfo.name
        url = f"https://{userName}.booth.pm"
        self._installFakeHeaderOpener()
        reqStr = req.urlopen(url=url, timeout=10) \
            .read() \
            .decode("utf-8")
        reqHtml = etree.HTML(reqStr)
        return reqHtml.xpath(self.PRODUCT_XPATH)
    
    def _updateGoods(self) -> list[str]:
        """
            Updates the old goods' list with the new one.
        
        ------

        returns:

        `list[str]`: Goods that differs new list from the old one
        """
        oldGoods = self._userInfo.goods
        newGoods = self._getWebsiteInfo()
        diffGoods = []
        for newGood in newGoods:
            if newGood not in oldGoods:
                diffGoods.append(newGood)
        self._userInfo.goods = newGoods
        return diffGoods
    
    def _updateTimestamp(self) -> None:
        """
            Updates the timestamp of the user with the current time.
        """
        self._userInfo.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def updateUserInfo(self) -> dict[str, list[str]] :
        """
            Updates the user info with the new one.

            ------

            returns:

            `dict[str, list[str]]`: the updated user info that gets into the notifier
        """
        diffGoods = self._updateGoods()
        self._updateTimestamp()
        return {self._userInfo.name: diffGoods}
