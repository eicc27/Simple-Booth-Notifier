from GoodsDTO import GoodsDTO
from strformat import StrFormat

class BoothNotifier:

    @staticmethod
    def notifyCrawlingStarter(userName: str):
        print("Starting updating for " + StrFormat.functional(userName))

    @staticmethod
    def notifyInfoLauncher(launchInfo: dict[str, list[GoodsDTO]]):
        """
            Launches the notification.
        """
        for userName, goods in launchInfo.items():
            coloredUserName = StrFormat.cstr(userName, style="UNDERLINE", fcolor="CYAN")
            if goods:
                print(f"New products for {coloredUserName}:")
                for good in goods:
                    good.logGoodsInfo()
            else:
                StrFormat.warning(f"Nothing to update for {userName}.")