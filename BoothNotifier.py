from strformat import StrFormat

class BoothNotifier:

    FAVORED_TYPE = "抱き枕カバー"

    @staticmethod
    def notifyCrawlingStarter(userName: str):
        print("Starting updating for " + StrFormat.functional(userName))

    @staticmethod
    def notifyInfoLauncher(launchInfo: dict[str, list[tuple[str, str, bool]]]):
        """
            Launches the notification.
        """
        for userName, goods in launchInfo.items():
            coloredUserName = StrFormat.cstr(userName, style="UNDERLINE", fcolor="CYAN")
            if goods:
                print(f"{coloredUserName}'s new goods:")
                for good in goods:
                    goodsName, goodsType, soldOut = good
                    goodsNameColor = "BLACK" if soldOut else "MAGENTA"
                    goodsNameStyle = "BOLD" if goodsType == BoothNotifier.FAVORED_TYPE else "DEFAULT"
                    goodsTypeStyle = goodsNameStyle
                    goodsTypeColor = "BLUE" if goodsType == BoothNotifier.FAVORED_TYPE else "BLACK"
                    coloredGoodsName = StrFormat.cstr(goodsName, style=goodsNameStyle, fcolor=goodsNameColor)
                    coloredGoodsType = StrFormat.cstr(goodsType, style=goodsTypeStyle, fcolor=goodsTypeColor)
                    if not soldOut:
                        print(f"{coloredGoodsName} ==> {coloredGoodsType}")
                    else:
                        coloredSoldOut = StrFormat.cstr("Sold Out", style="BOLD", fcolor="RED")
                        print(f"{coloredGoodsName} ==> {coloredGoodsType} ({coloredSoldOut})")
            else:
                StrFormat.warning(f"Nothing to update for {userName}.")