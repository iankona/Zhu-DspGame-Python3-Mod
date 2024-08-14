
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


显示标签 = False
显示文本 = ""
百分比 = 0.0
屏幕位置 = Vector3.zero

按住时间 = 1.5


def 函数():
    global 显示标签, 屏幕位置
    if UIRoot.instance == None: return
    if GameMain.mainPlayer == None: return
    if GameMain.sandboxToolsEnabled == True: return
    if UIGame.viewMode != EViewMode.Starmap: return

    starmap = UIRoot.instance.uiGame.starmap

    if Input.GetMouseButtonDown(1): # 右键按下
        显示标签 = True
        屏幕位置.x = Input.mousePosition.x
        屏幕位置.y = Screen.height - Input.mousePosition.y
        starmap.screenCameraController.SetRotationLock(False)
        Traverse.Create(starmap).Method("ResetRightClickFastTravelVars").GetValue() # starmap.ResetRightClickFastTravelVars()
        Traverse.Create(starmap).Field("fastTravelRightDownMousePos").SetValue(Input.mousePosition)
        starmap.fastTravelRightPressing = True

    if Input.GetMouseButton(1): # 右键按住
        显示标签 = True
        fastTravelRightDownMousePos = Traverse.Create(starmap).Field("fastTravelRightDownMousePos").GetValue()
        starmap.fastTravelRightPressing = True
        starmap.fastTravelRightDownTime += Time.deltaTime
        if (Input.mousePosition - fastTravelRightDownMousePos).sqrMagnitude > 64.0 and starmap.fastTravelRightDownTime < 0.0:
            显示标签 = False
            starmap.fastTravelRightPressing = False

    if Input.GetMouseButtonUp(1): #
        显示标签 = False
        Traverse.Create(starmap).Method("ResetRightClickFastTravelVars").GetValue() # starmap.ResetRightClickFastTravelVars()

    if starmap.fastTravelRightPressing and starmap.fastTravelRightDownTime > 0.0:
        Locic()

    if starmap.fastTravelRightDownTime > 按住时间 and starmap.fastTravelRightDownTime < 按住时间+1.0:
        显示标签 = False
        DoRightClickFastTravel()

    if starmap.fastTravelRightDownTime > 按住时间+1.0:
        Traverse.Create(starmap).Method("ResetRightClickFastTravelVars").GetValue() # starmap.ResetRightClickFastTravelVars()

    



def Locic():
    global 百分比, 显示文本
    starmap = UIRoot.instance.uiGame.starmap

    Traverse.Create(starmap).Method("CalcRightClickFastTravelTarget", [Input.mousePosition]).GetValue()

    target, targetStar, targetPlanet = _target(), _targetStar(), _targetPlanet()

    百分比 = (int)(starmap.fastTravelRightDownTime / 按住时间 * 100)
    if 百分比 > 100: 百分比 = 100

    if targetPlanet != None:
        显示文本 = f"准备快速传送\n目标行星：{targetPlanet.displayName}\n进度：{百分比}%"
        target = targetPlanet.uPosition
    elif targetStar != None:
        显示文本 = f"准备快速传送\n目标星系：{targetStar.displayName}\n进度：{百分比}%"
        target = targetStar.uPosition
    else:
        显示文本 = f"准备快速传送\n目标位置：深空（{target}）\n进度：{百分比}%"


def DoRightClickFastTravel():
    starmap = UIRoot.instance.uiGame.starmap

    target, targetStar, targetPlanet = _target(), _targetStar(), _targetPlanet()
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



def _target():
    starmap = UIRoot.instance.uiGame.starmap
    target = Traverse.Create(starmap).Field("fastTravelRightTarget").GetValue()
    return target

def _targetStar():
    starmap = UIRoot.instance.uiGame.starmap
    targetStar = Traverse.Create(starmap).Field("fastTravelRightTargetStar").GetValue()
    return targetStar

def _targetPlanet():
    starmap = UIRoot.instance.uiGame.starmap
    targetPlanet = Traverse.Create(starmap).Field("fastTravelRightTargetPlanet").GetValue()
    return targetPlanet


def ImGUI():
    if 显示标签 == False: return  
    rect = Rect(屏幕位置.x + 20, 屏幕位置.y - 80, 500, 80)

    labelStyle = GUIStyle(GUI.skin.label)
    labelStyle.fontSize = 18

    GUI.Label(rect, 显示文本, labelStyle)