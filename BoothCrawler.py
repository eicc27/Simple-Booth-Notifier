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
    PRODUCT_TYPE_XPATH = "//div[@class=\"item-category\"]/text()"

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

    def _getWebsiteInfo(self) -> tuple[list[str], list[str], list[bool]]:
        """
            Reaches the target website to get the goods list.
        
        ------

        returns:

        `tuple[list[str], list[str], list[bool]]`: the goods list, the type of the goods, and the availability of the goods
        """
        userName = self._userInfo.name
        url = f"https://{userName}.booth.pm"
        self._installFakeHeaderOpener()
        reqStr = req.urlopen(url=url, timeout=10) \
            .read() \
            .decode("utf-8")
        reqHtml = etree.HTML(reqStr)
        products = reqHtml.xpath(self.PRODUCT_XPATH)
        types = reqHtml.xpath(self.PRODUCT_TYPE_XPATH)
        isSoldOut: list[bool] = []
        for i, _ in enumerate(products):
            soldOut = reqHtml.xpath(f"//shop-item-component[{i+1}]//div[@class=\"badge empty-stock\"]/text()")
            isSoldOut.append(True if soldOut else False)
        return products, types, isSoldOut
    
    def _updateGoods(self) -> list[tuple[str, str, bool]]:
        """
            Updates the old goods' list with the new one.
        
        ------

        returns:

        `list[tuple[str, str, bool]]`: the difference between the old and new goods' list
        """
        oldGoods = self._userInfo.goods
        newGoods, goodTypes, isSoldOut = self._getWebsiteInfo()
        diffGoods: list[tuple[str, str]] = []
        for newGood, goodType, soldOut in zip(newGoods, goodTypes, isSoldOut):
            if newGood not in oldGoods:
                diffGoods.append((newGood, goodType, soldOut))
        self._userInfo.goods = newGoods
        return diffGoods
    
    def _updateTimestamp(self) -> None:
        """
            Updates the timestamp of the user with the current time.
        """
        self._userInfo.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def updateUserInfo(self) -> dict[str, list[tuple[str, str, bool]]] :
        """
            Updates the user info with the new one.

            ------

            returns:

            `dict[str, list[tuple[str, str, bool]]]`: the difference between the old and new goods' list
        """
        diffGoods = self._updateGoods()
        self._updateTimestamp()
        return {self._userInfo.name: diffGoods}
