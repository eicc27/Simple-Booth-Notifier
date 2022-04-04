from SyncHistory import SyncHistory
from BoothCrawler import BoothCrawler
from BoothNotifier import BoothNotifier
from strformat import StrFormat

if __name__ == "__main__":
    syncHistory = SyncHistory()
    boothNotifier = BoothNotifier()
    for i, userInfo in enumerate(syncHistory):
        boothcrawler = BoothCrawler(userInfo)
        boothNotifier.notifyCrawlingStarter(userInfo.name)
        infoNotifier = boothcrawler.updateUserInfo()
        syncHistory[i] = boothcrawler.userInfo
        syncHistory.writeBack()
        boothNotifier.notifyInfoLauncher(infoNotifier)
    StrFormat.ok("Done!")