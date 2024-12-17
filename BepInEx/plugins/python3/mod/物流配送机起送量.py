

from dsptype import GameHistoryData, DispenserComponent
from dspharmony import HarmonyPatch_Postfix_Default, HarmonyPatch_Prefix_DefaultAndResult



def Start():
    HarmonyPatch_Postfix_Default(GameHistoryData, "UnlockTechFunction", postfunc=Postfix) # void UnlockTechFunction(int func, double value, int level)
    HarmonyPatch_Prefix_DefaultAndResult(DispenserComponent, "PickFromStoragePrecalc", prefunc=Prefix_Boolean, preresult=Prefix_Result) # int PickFromStoragePrecalc(int itemId, int needCnt)


def Update():
    pass

def OnGUI():
    pass



carries = 100
def Postfix(__instance, func, value, level): # 解锁全球送
    if __instance.logisticCourierCarries < carries: __instance.logisticCourierCarries = carries # 运载量
    __instance.dispenserDeliveryMaxAngle = 180 # 配送角度


def Prefix_Result(__instance, itemId, needCnt, __result):
    if needCnt < carries: __result = 0
    return __result

def Prefix_Boolean(__instance, itemId, needCnt):
    if needCnt < carries: return False
    return True

