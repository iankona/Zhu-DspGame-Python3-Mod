import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetFactory, VeinData, GameMain, MinerComponent, PowerSystem, PrefabDesc
from dspharmony import HarmonyPatchDefaultPostfix, HarmonyPatchParameterPrefix, HarmonyPatchParameterPostfixWithReturn
from UnityEngine import Vector3, Time, Quaternion, MeshRenderer, MotionVectorGenerationMode, Material, Color, Component, MeshFilter, Mesh
 
from UnityEngine.Rendering import ShadowCastingMode



def Start():
    HarmonyPatchParameterPostfixWithReturn(PowerSystem, "NewGeneratorComponent", System.Int32, [System.Int32, PrefabDesc], Postfix)


def Update():
    pass

def OnGUI():
    pass



发电建筑列表 = [
    2203, # 风力涡轮机
    2205, # 太阳能板
    2213, # 地热发电站

]



def Postfix(__instance, entityId, desc, __result):
    itemProtoID = __instance.factory.entityPool[entityId].protoId
    if itemProtoID in 发电建筑列表:
        __instance.genPool[__result].genEnergyPerTick = 10 * desc.genEnergyPerTick
    return __result




# 2203, # 风力涡轮机
# 2204, # 火力发电厂
# 2205, # 太阳能板
# 2211, # 微型聚变发电站
# 2213, # 地热发电站
