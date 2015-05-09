# AutoSync Addon for Anki
# Author: ftechz <github.com/ftechz/anki-autosync>

# Automatically synchronise the decks when idle for a certain period

from aqt import mw
from anki.hooks import addHook

IDLE_PERIOD = 15
RETRY_PERIOD = 2

class AutoSync:
    def syncDecks(self):
        """Force sync if in any of the below states"""
        self.timer = None
        if mw.state in ["deckBrowser", "overview", "review"]:
            mw.onSync()
        else:
            # Not able to sync. Wait another 2 minutes
            self.startSyncTimer(self.retryPeriod)

    def startSyncTimer(self, minutes):
        """Start/reset the timer to sync deck"""
        if self.timer is not None:
            self.timer.stop()
        self.timer = mw.progress.timer(1000*60 * minutes, self.syncDecks, False)

    def resetTimer(self, minutes):
        """Only reset timer if the timer exists"""
        if self.timer is not None:
            self.startSyncTimer(minutes)

    def updatedHook(self, *args):
        """Start/restart timer to trigger if idle for a certain period"""
        self.startSyncTimer(self.idlePeriod)

    def activityHook(self, *args):
        """Reset the timer if there is some kind of activity"""
        self.resetTimer(self.idlePeriod)

    def __init__(self):
        self.idlePeriod = IDLE_PERIOD
        self.retryPeriod = RETRY_PERIOD
        self.timer = None

        updatedHooks = [
            "showQuestion",
            "reviewCleanup",
            "editFocusGained",
            "noteChanged",
            "reset",
            "tagsUpdated"
        ]

        activtyHooks = [
            "showAnswer",
            "newDeck"
            ]

        for hookName in updatedHooks:
            addHook(hookName, self.updatedHook)

        for hookName in activtyHooks:
            addHook(hookName, self.activityHook)

AutoSync()
