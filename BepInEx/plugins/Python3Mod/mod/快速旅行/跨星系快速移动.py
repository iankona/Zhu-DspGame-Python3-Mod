
from dsptype import GameMain, UIGame, UIRoot, UIBuildMenu, EViewMode, VectorLF3
from UnityEngine import Input, Time, Vector3, Vector2, Mathf, Screen
from UnityEngine import Rect, GUI, GUIStyle, GUIContent
from System import String

from HarmonyLib import Traverse


# private void ResetRightClickFastTravelVars()
# {
#     this.fastTravelRightDownMousePos = Vector3.zero;
#     this.fastTravelRightPressing = false;
#     this.fastTravelRightDownTime = -0.25f;
#     this.fastTravelRightTarget = VectorLF3.zero;
#     this.fastTravelRightTargetStar = (StarData) null;
#     this.fastTravelRightTargetPlanet = (PlanetData) null;
# }


屏幕位置 = Vector2.zero
显示文本 = ""
按住时间 = 1.5


def 函数():
    if UIRoot.instance == None: return
    if GameMain.mainPlayer == None: return
    if GameMain.sandboxToolsEnabled == True: return
    if UIGame.viewMode != EViewMode.Starmap: return

    starmap = UIRoot.instance.uiGame.starmap

    if Input.GetMouseButtonDown(1): # 右键按下
        starmap.screenCameraController.SetRotationLock(False)
        MousePositionTo屏幕坐标(Input.mousePosition)
        ResetRightClickFastTravelVars()
        SetFastTravelRightDownMousePos(Input.mousePosition)
        CalcRightClickFastTravelTarget(Input.mousePosition)
        starmap.fastTravelRightPressing = True

    if Input.GetMouseButton(1) and starmap.fastTravelRightPressing: # 右键按住 
        starmap.fastTravelRightDownTime += Time.deltaTime
        更新显示文本()
        rightMousePosition = GetFastTravelRightDownMousePos()
        if (Input.mousePosition - rightMousePosition).sqrMagnitude > 64.0: ResetRightClickFastTravelVars()

    if Input.GetMouseButtonUp(1): #
        ResetRightClickFastTravelVars()

    if starmap.fastTravelRightDownTime > 按住时间 and starmap.fastTravelRightPressing:
        DoRightClickFastTravel()
        ResetRightClickFastTravelVars()

    
def 更新显示文本():
    global 显示文本
    starmap = UIRoot.instance.uiGame.starmap
    target, targetStar, targetPlanet = GetTargetStarPlanet()
    百分比 = (int)(starmap.fastTravelRightDownTime / 按住时间 * 100)
    if 百分比 < 0  : 百分比 = 0
    if 百分比 > 100: 百分比 = 100
    if targetPlanet != None:
        显示文本 = f"准备快速传送\n目标行星：{targetPlanet.displayName}\n进度：{百分比}%"
    elif targetStar != None:
        显示文本 = f"准备快速传送\n目标星系：{targetStar.displayName}\n进度：{百分比}%"
    else:
        显示文本 = f"准备快速传送\n目标位置：深空 [{int(target.x)}, {int(target.y)}, {int(target.z)}] \n进度：{百分比}%"
    


def MousePositionTo屏幕坐标(mousePosition:Vector3):
    global 屏幕位置
    屏幕位置.x = mousePosition.x                 # 屏幕位置.x = Input.mousePosition.x
    屏幕位置.y = Screen.height - mousePosition.y # 屏幕位置.y = Screen.height - Input.mousePosition.y


def ResetRightClickFastTravelVars():
    starmap = UIRoot.instance.uiGame.starmap
    Traverse.Create(starmap).Method("ResetRightClickFastTravelVars").GetValue() # starmap.ResetRightClickFastTravelVars()


def SetFastTravelRightDownMousePos(mousePosition):
    starmap = UIRoot.instance.uiGame.starmap
    Traverse.Create(starmap).Field("fastTravelRightDownMousePos").SetValue(Input.mousePosition)


def GetFastTravelRightDownMousePos():
    starmap = UIRoot.instance.uiGame.starmap
    result = Traverse.Create(starmap).Field("fastTravelRightDownMousePos").GetValue()
    return result


def CalcRightClickFastTravelTarget(mousePosition) -> bool: # Vector3
    starmap = UIRoot.instance.uiGame.starmap
    calcflag = Traverse.Create(starmap).Method("CalcRightClickFastTravelTarget", [mousePosition]).GetValue()
    return calcflag




def DoRightClickFastTravel():
    starmap = UIRoot.instance.uiGame.starmap
    target, targetStar, targetPlanet = GetTargetStarPlanet()
    if targetPlanet != None:
        starmap.SetViewStar(targetStar)
        starmap.screenCameraController.SetViewTarget(targetPlanet, None, None, GameMain.mainPlayer, VectorLF3.zero, 0.2, 1.0, False, False)
    elif targetStar != None:
        starmap.SetViewStar(targetStar, True)
        starmap.screenCameraController.SetViewTarget(None, targetStar, None, GameMain.mainPlayer, VectorLF3.zero, targetStar.physicsRadius * 0.00025, targetStar.physicsRadius * 0.00025 * 5.0, False, False)
    else:
        starmap.screenCameraController.DisablePositionLock()

    if targetPlanet != None:
         StartFastTravelToPlanet(targetPlanet)
    else:
         StartFastTravelToUPosition(target)


def StartFastTravelToPlanet(destPlanet): # PlanetData
    GameMain.mainPlayer.controller.actionSail.StartFastTravelToPlanet(destPlanet)


def StartFastTravelToUPosition(uPos): # VectorLF3 
    GameMain.mainPlayer.controller.actionSail.StartFastTravelToUPosition(uPos)



def GetTargetStarPlanet():
    starmap = UIRoot.instance.uiGame.starmap
    target = Traverse.Create(starmap).Field("fastTravelRightTarget").GetValue()
    targetStar = Traverse.Create(starmap).Field("fastTravelRightTargetStar").GetValue()
    targetPlanet = Traverse.Create(starmap).Field("fastTravelRightTargetPlanet").GetValue()
    return target, targetStar, targetPlanet


def ImGUI():
    starmap = UIRoot.instance.uiGame.starmap
    if starmap.fastTravelRightPressing == False: return  

    rect = Rect(屏幕位置.x + 20, 屏幕位置.y - 100, 500, 100)

    labelStyle = GUIStyle(GUI.skin.label)
    labelStyle.fontSize = 20

    GUI.Label(rect, 显示文本, labelStyle)