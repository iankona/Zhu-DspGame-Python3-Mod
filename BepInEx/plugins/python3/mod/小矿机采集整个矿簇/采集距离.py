import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import NearColliderLogic, MinerComponent
from dspharmony import HarmonyPatch_Static_Prefix_Result

from UnityEngine import Vector3, Mathf

from .CSharpCode距离 import HarmonyPatch_Prefix_Parameter



def Start():
    HarmonyPatch_Prefix_Parameter(NearColliderLogic, "GetVeinsInAreaNonAlloc", preparameter=Prefix0) # int GetVeinsInAreaNonAlloc(Vector3 center, float areaRadius, ref int[] veinIds)
    HarmonyPatch_Static_Prefix_Result(MinerComponent, "IsTargetVeinInRange", preresult=Prefix1) # static bool IsTargetVeinInRange(Vector3 vPos, Pose lPose, PrefabDesc desc) # 是静态函数，需要注意区别处理


def Prefix0(__instance, center, areaRadius, veinIds):
    areaRadius = 18.0
    return areaRadius


# 修改的是静态方法，所以没有__instance
def Prefix1(vPos, lPose, desc, __result):
    __result = True
    forward = lPose.forward
    if desc.veinMiner:
        if desc.isVeinCollector:
            vector3 = lPose.position + forward * (-10.0)
            rhs = -forward
            right = lPose.right
            lhs = vPos - vector3
            sqrMagnitude = lhs.sqrMagnitude
            num1 = Mathf.Abs(Vector3.Dot(lhs, rhs))
            num2 = Mathf.Abs(Vector3.Dot(lhs, right))
            if sqrMagnitude > 100.0 or num1 > 7.75 or num2 > 6.25: 
                __result = False
        else:
            vector3_1 = lPose.position + forward * -1.2
            rhs1 = -forward
            up = lPose.up
            rhs2 = vPos - vector3_1
            f = Vector3.Dot(up, rhs2)
            vector3_2 = rhs2 - up * f
            sqrMagnitude = vector3_2.sqrMagnitude
            num = Vector3.Dot(vector3_2.normalized, rhs1)
            # 小采矿机的判断代码, 删除距离过长判断
            if num < 0.73000001907348633 or Mathf.Abs(f) > 2.0:  #  or sqrMagnitude > 961.0 / 16.0:
                __result = False  
    return __result
    