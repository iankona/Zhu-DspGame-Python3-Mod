import System

from dsptype import PlanetFactory, BuildTool_Click, BuildTool_Path, ConstructionSystem
from dspharmony import HarmonyPatchDefaultPrefixWithReturn, HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix
from UnityEngine import Vector3

def Start():
    HarmonyPatchDefaultPrefixWithReturn(PlanetFactory, "FlattenTerrain", System.Int32, PrefixReturn, System.Boolean, PrefixBoolean) # 禁用地形修改函数
    HarmonyPatchDefaultPostfix(BuildTool_Path, "DeterminePreviews", Postfix) # 提升 传送带 至星球地面
    HarmonyPatchDefaultPostfix(BuildTool_Click, "DeterminePreviews", Postfix) # 提升 建筑 至星球地面

    HarmonyPatchDefaultPrefix(BuildTool_Path, "CreatePrebuilds", Prefix) # 提升 传送带 至星球地面
    HarmonyPatchDefaultPrefix(BuildTool_Click, "CreatePrebuilds", Prefix) # 提升 建筑 至星球地面



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
        magnitude = buildPreview.lpos.magnitude
        height = __instance.planet.data.QueryHeight(buildPreview.lpos)
        height2 = __instance.planet.data.QueryHeight(buildPreview.lpos2)
        if  magnitude < __instance.planet.radius or magnitude > height: continue
        buildPreview.lpos = buildPreview.lpos.normalized * height
        buildPreview.lpos2 = buildPreview.lpos2.normalized * height2



def Prefix(__instance):
    for buildPreview in __instance.buildPreviews:
        vec1 = buildPreview.lpos
        tmp_ids = System.Array.CreateInstance(System.Int32, 1024) # int[] a = new int[1024]; #  print(tmp_ids) # System.Int32[]
        num = __instance.planet.physics.nearColliderLogic.GetVegetablesInAreaNonAlloc(vec1, 5.0, tmp_ids) # 注意函数参数没有 ref 不能写成 num, ids = ... ... 形式 # 比起遍历 vegePool, 可大幅度减少计算量 # print(f"{num}: {ids}") # 12: System.Int32[] 
        for i in range(num): 
            id = tmp_ids[i]
            vege = __instance.factory.vegePool[id]
            if vege.id == 0: continue
            vec2 = vege.pos
            if Vector3.Distance(vec1, vec2) < 5.0: __instance.factory.RemoveVegeWithComponents(vege.id)
    return True
