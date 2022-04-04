from datetime import datetime
from urllib import request as req
from lxml import etree
from fake_useragent import UserAgent
from GoodsDTO import GoodsDTO
from UserInfo import UserInfo

class BoothCrawler:
    """
    Given a URL pointing to a user, and a synchronization history with a timestamp,
    the class tries to update that local history.
    
    ------

    parameters: 
    
    `userInfo`: `UserInfo`: the user info to be updated
    """

    PRODUCT_URL_XPATH = "//li/@data-product-id"
    PRODUCT_TYPE_XPATH = "//div[@class=\"item-category\"]/text()"
    PRODUCT_NAME_XPATH = "//h2[@class=\"item-name\"]//a/text()"
    EXAMPLE_INDEX = "234"
    PRODUCT_STATUS_XPATH = f"//shop-item-component[{EXAMPLE_INDEX}]//div[@class=\"badge empty-stock\"]/text()"
    

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

    def _ExtendUrlID(self, urlID: str) -> str:
        return f"https://{self.userInfo.userName}.booth.pm/items/{urlID}"

    def _getWebsiteInfo(self) -> tuple[list[GoodsDTO], list[str]]:
        """
            Reaches the target website to get the goods list.
        
            Returns
            ------

            `tuple[list[GoodsDTO], list[str]]`: the goods list and the url-ID list
        """
        userName = self._userInfo.userName
        url = f"https://{userName}.booth.pm"
        self._installFakeHeaderOpener()
        reqStr = req.urlopen(url=url, timeout=10) \
            .read() \
            .decode("utf-8")
        reqHtml = etree.HTML(reqStr)
        urlIDs: list[str] = reqHtml.xpath(self.PRODUCT_URL_XPATH)
        urls = [self._ExtendUrlID(urlID) for urlID in urlIDs] # the complete, reachable url
        types: list[str] = reqHtml.xpath(self.PRODUCT_TYPE_XPATH)
        names: list[str] = reqHtml.xpath(self.PRODUCT_NAME_XPATH)
        isSoldOut: list[bool] = []
        for i, _ in enumerate(urlIDs):
            soldOut = reqHtml.xpath(self.PRODUCT_STATUS_XPATH.\
                replace(self.EXAMPLE_INDEX, str(i + 1)))
            isSoldOut.append(True if soldOut else False)
        return [GoodsDTO(name=name, url=url, type=type, soldOut=soldOut) \
            for name, url, type, soldOut in zip(names, urls, types, isSoldOut)], \
            urlIDs

    def _updateGoods(self) -> list[GoodsDTO]:
        """
            Updates the old goods' list with the new one, and returns the difference.
        
            Returns
            ------

            `list[GoodsDTO]`: the difference between the old and new goods' list
        """
        oldIDs = self._userInfo.goodIDs
        newGoods, newIDs = self._getWebsiteInfo()
        diffGoods: list[GoodsDTO] = []
        for newGood, newID in zip(newGoods, newIDs):
            if newID not in oldIDs:
                diffGoods.append(newGood)
        self._userInfo.goodIDs = newIDs
        return diffGoods
    
    def _updateTimestamp(self) -> None:
        """
            Updates the timestamp of the user with the current time.
        """
        self._userInfo.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def updateUserInfo(self) -> dict[str, list[GoodsDTO]] :
        """
            Updates the user info with the new one.

            Returns
            ------

            `dict[str, list[GoodsDTO]]`: the difference between the old and new goods' list
        """
        diffGoods = self._updateGoods()
        self._updateTimestamp()
        return {self._userInfo.userName: diffGoods}
