from strformat import StrFormat

class GoodsDTO:
    """
        Data Transfer Object for filing Goods info while crawling.

        Main function: `logGoodsInfo`

        All accepted parameters are positional.

        Parameters
        ------
        `name`: `str`, the name of the goods.

        `url`: `str`, the exact url of the goods({user}.booth.pm/items/{url_id}). Readable.
        
        `type`: `str`, the type of the goods.

        `soldOut`: `bool`, whether the goods is sold out.
    """

    FAVORED_TYPE = ["抱き枕カバー", ]

    def __init__(self, *, name: str, url: str, type: str, soldOut: bool) -> None:
        self._name = name
        self._url = url
        self._type = type
        self._soldOut = soldOut
    

    @property
    def url(self) -> str:
        return self._url
    
    def logGoodsInfo(self) -> None:
        """
        Prints the colored info of the goods. If `soldOut`, all styles will fall back to default.
        
        Otherwise, cases are listed below:

        > Colors
        ------

        The `name` is `BLACK` by default. If `type` is `FAVORED_TYPE`, `CYAN` instead.

        The `url` is `BLACK` by default. If `type` is `FAVORED_TYPE`, `YELLOW` instead.

        The `type` is `BLACK` by default. If `FAVORED_TYPE`, `BLUE` instead.


        > Style
        ------

        The `name`, `url`, and `type` are `DEFAULT` by default. If `FAVORED_TYPE`, `BOLD` instead.

        The `type` is `DEFAULT` by default. If `FAVORED_TYPE`, `REVERSE` instead.

        > Format
        ------

        If not `soldOut`, f"{url} ==> {name}, {type}"

        Else, f"{url} ==> {name}, {type} (Sold Out)" where "Sold Out" is `BOLD`, `RED`.
        """
        if self._soldOut:
            soldOutStr = StrFormat.cstr("Sold Out", style="BOLD", fcolor="RED")
            print(f"{self._url} ==> {self._name}, {self._type} ({soldOutStr})")
            return
        isFavored = self._type in GoodsDTO.FAVORED_TYPE
        nameColor = "CYAN" if isFavored else "BLACK"
        urlColor = "YELLOW" if isFavored else "BLACK"
        typeColor = "BLUE" if isFavored else "BLACK"
        nameStyle = urlStyle = "BOLD" if isFavored else "DEFAULT"
        typeStyle = "REVERSE" if isFavored else "DEFAULT"
        coloredName = StrFormat.cstr(self._name, style=nameStyle, fcolor=nameColor)
        coloredUrl = StrFormat.cstr(self._url, style=urlStyle, fcolor=urlColor)
        coloredType = StrFormat.cstr(self._type, style=typeStyle, fcolor=typeColor)
        print(f"{coloredUrl} ==> {coloredName}, {coloredType}")




