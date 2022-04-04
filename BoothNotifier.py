from strformat import StrFormat

class BoothNotifier:

    @staticmethod
    def notifyCrawlingStarter(userName: str):
        print("Starting updating for " + StrFormat.functional(userName))

    @staticmethod
    def notifyInfoLauncher(launchInfo: dict[str, list[str]]):
        """
            Launches the notification.
        """
        for userName, goods in launchInfo.items():
            coloredUserName = StrFormat.cstr(userName, style="UNDERLINE", fcolor="CYAN")
            if goods:
                print(f"{coloredUserName}'s new goods:")
                for good in goods:
                    goodsName, goodsType = good
                    coloredGoodsName = StrFormat.cstr(goodsName, style="BOLD", fcolor="MAGENTA")
                    coloredGoodsType = StrFormat.cstr(goodsType, style="DEFAULT", fcolor="GREEN")
                    print(f"{coloredGoodsName} ==> {coloredGoodsType}")
            else:
                StrFormat.warning(f"Nothing to update for {userName}.")