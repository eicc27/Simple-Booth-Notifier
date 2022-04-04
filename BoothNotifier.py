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
            coloredGoods = StrFormat.cstr(",".join(goods), style="DEFAULT", fcolor="RED")
            if goods:
                print(f"{coloredUserName}'s new goods: {coloredGoods}.")
            else:
                StrFormat.warning(f"Nothing to update for {userName}.")