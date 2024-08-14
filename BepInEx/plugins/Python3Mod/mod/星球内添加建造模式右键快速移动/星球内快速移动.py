
from dsptype import GameMain, UIGame, UIRoot, UIBuildMenu, EViewMode



def 函数():
    建造视图()
    全球视图()



def 建造视图():
    if UIRoot.instance == None: return
    if UIGame.viewMode == EViewMode.Build or UIGame.viewMode == EViewMode.Normal:
        UIRoot.instance.uiGame.globemap.TeleportLogic()



def 全球视图():
    if UIRoot.instance == None: return
    if GameMain.sandboxToolsEnabled == True: return
    if UIGame.viewMode == EViewMode.Globe:
        UIRoot.instance.uiGame.globemap.TeleportLogic()