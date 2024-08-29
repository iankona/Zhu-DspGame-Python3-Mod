import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetFactory, VeinData, GameMain, MinerComponent, PowerSystem, PrefabDesc, GameHistoryData, DispenserComponent
from dspharmony import HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix, HarmonyPatchParameterPrefix, HarmonyPatchParameterPrefixWithReturn

from . import CSharpCode

def Start():
    CSharpCode.HarmonyPatchDefaultPrefixWithRefParameter(MinerComponent, "InitVeinArray", System.Int32, Prefix0)
    HarmonyPatchDefaultPrefix(MinerComponent, "ArrangeVeinArray", Prefix1)


def Update():
    pass

def OnGUI():
    pass



def Prefix0(__instance, vcnt):
    vcnt = 32
    return vcnt


def Prefix1(__instance):
    entity = GameMain.mainPlayer.factory.entityPool[__instance.entityId]
    if entity.protoId == 2301: 小矿机添加矿脉(__instance) # 小矿机
    return True


 
def 小矿机添加矿脉(__instance):
    veinPool = GameMain.mainPlayer.factory.veinPool
    veinCursor = GameMain.mainPlayer.factory.veinCursor

    index0 = __instance.veins[0]
    vein = veinPool[index0]
    left, right = index0-32, index0+32
    if left < 1: left = 1
    if right >= veinCursor: right = veinCursor

    矿脉列表 = []
    for i in range(left, right):
        child_vein = veinPool[i]
        if vein.groupIndex == child_vein.groupIndex: 矿脉列表.append(child_vein.id) # 实际上 i == child_vein.id

    System.Array.Clear(__instance.veins, 0, 32)
    for i, id in enumerate(矿脉列表): __instance.veins[i] = id

    
 
 
 