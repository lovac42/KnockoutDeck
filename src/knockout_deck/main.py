# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/KnockoutDeck
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import aqt
from aqt.qt import *
from aqt import mw
from anki.hooks import wrap
from .studydeck import StudyDeck
from .const import *
from .config import *


class KnockoutDeck:
    loaded=False

    def __init__(self):
        self.conf=Config(ADDON_NAME)
        addHook(ADDON_NAME+".configLoaded", self.onConfigLoaded)


    def onConfigLoaded(self):
        if not self.loaded:
            self.setupMenu()
            self.loaded=True


    def setupMenu(self):
        menu=None
        for a in mw.form.menubar.actions():
            if '&Study' == a.text():
                menu=a.menu()
                menu.addSeparator()
                break
        if not menu:
            menu=mw.form.menubar.addMenu('&Study')

        item=QAction("Knockout Deck", mw)
        item.triggered.connect(self.show)
        key=self.conf.get("hotkey",None)
        if key: item.setShortcut(QKeySequence(key))
        menu.addAction(item)


    def show(self):
        sd=StudyDeck(mw, title="Knockout Deck",
            dyn=False, current=mw.col.decks.current()['name'])
        if sd.name: #not canceled
            dids=sd.getSelectedDids()
            mw.col.decks.select(dids[0])
            mw.col.conf['activeDecks']=dids
            mw.moveToState("overview")


ko_deck=KnockoutDeck()

