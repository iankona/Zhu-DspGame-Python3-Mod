
from HarmonyLib import Traverse

from dsptype import UIGalaxySelect
from dspharmony import HarmonyPatch_Prefix_Default, HarmonyPatch_Postfix_Default


def Start():
    HarmonyPatch_Postfix_Default(UIGalaxySelect, "_OnOpen", postfunc=Postfix) # void _OnOpen()
    HarmonyPatch_Prefix_Default(UIGalaxySelect, "OnStarCountSliderValueChange", prefunc=Prefix) # void OnStarCountSliderValueChange(float val)


def Update():
    pass

def OnGUI():
    pass


# Only in [7, 247]
minstarcount = 7    # 小于   7 个，会报错
maxstarcount = 247  # 大于 247 个，会报错
def Postfix(__instance):
    starCountSlider = Traverse.Create(__instance).Field("starCountSlider").GetValue()
    starCountSlider.minValue = minstarcount
    starCountSlider.maxValue = maxstarcount


def Prefix(__instance, val):
    gameDesc = Traverse.Create(__instance).Field("gameDesc").GetValue()
    starCountSlider = Traverse.Create(__instance).Field("starCountSlider").GetValue()
    num = int(starCountSlider.value + 0.10000000149011612)
    if num < minstarcount: num = minstarcount
    if num > maxstarcount: num = maxstarcount
    if num == gameDesc.starCount: return False # 查看戴森球计划代码，要求是如此
    gameDesc.starCount = num
    __instance.SetStarmapGalaxy()
    return False # 拦截原函数