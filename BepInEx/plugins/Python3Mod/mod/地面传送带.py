import System

from dsptype import PlanetFactory, BuildTool_Click, BuildTool_Path
from dspharmony import HarmonyPatchDefaultPrefixWithReturn, HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix


def Start():
    HarmonyPatchDefaultPrefixWithReturn(PlanetFactory, "FlattenTerrain", System.Int32, PrefixReturn, System.Boolean, PrefixBoolean) # 禁用地形修改函数
    HarmonyPatchDefaultPostfix(BuildTool_Path, "DeterminePreviews", Postfix) # 提升 传送带 至星球地面
    HarmonyPatchDefaultPostfix(BuildTool_Click, "DeterminePreviews", Postfix) # 提升 建筑 至星球地面

def Update():
    pass

def OnGUI():
    pass

def PrefixReturn(__instance):
    return 0

def PrefixBoolean(__instance):
    return False


def Postfix(__instance):
    for buildPreview in __instance.buildPreviews:
        height = __instance.planet.data.QueryHeight(buildPreview.lpos)
        height2 = __instance.planet.data.QueryHeight(buildPreview.lpos2)
        buildPreview.lpos = buildPreview.lpos.normalized * height
        buildPreview.lpos2 = buildPreview.lpos2.normalized * height2


