import System
from HarmonyLib import AccessTools, Traverse

from dsptype import StorageComponent, LDB, GameMain
from dspharmony import HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix, HarmonyPatchDefaultPrefixAndPostfix, HarmonyPatchDefaultOriginalAndPrefixAndPostfix
from dspassembly import 程序集类型

from UnityEngine import Color

def Start():
    HarmonyPatchDefaultPostfix(StorageComponent, "LoadStatic", Postfix)
    HarmonyPatchDefaultPrefixAndPostfix(StorageComponent, "Sort", StoragePrefix, StoragePostfix)
    HarmonyPatchDefaultPrefixAndPostfix(StorageComponent, "AddItemStacked", StoragePrefix, StoragePostfix)
    HarmonyPatchDefaultOriginalAndPrefixAndPostfix(StorageComponent, "AddItem", AddItem(), StoragePrefix, StoragePostfix)


def Update():
    pass

def OnGUI():
    pass


multiplier = 10

olditemStackCount = None
newitemStackCount = None
def Postfix(__instance):
    global olditemStackCount, newitemStackCount
    olditemStackCount = StorageComponent.itemStackCount

    newitemStackCount = System.Array[System.Int32](12000)
    for i in range(12000): 
        newitemStackCount[i] = 1000

    for j in range(LDB.items.dataArray.Length):
        itemProto = LDB.items.dataArray[j]
        newitemStackCount[itemProto.ID] = multiplier * itemProto.StackSize



def StoragePrefix(__instance):
    if __instance == GameMain.data.mainPlayer.package: StorageComponent.itemStackCount = newitemStackCount
    return True

def StoragePostfix(__instance):
    if __instance == GameMain.data.mainPlayer.package: StorageComponent.itemStackCount = olditemStackCount


dspAssemblyType = 程序集类型(".\\DSPGAME_Data\\Managed\\Assembly-CSharp.dll", "StorageComponent")
def AddItem():
    # dspAssemblyType.PrintMethod("AddItem")
    return dspAssemblyType.FindMethod("AddItem")[4]

# 0:: Int32 AddItem(Int32, Int32, Int32, Int32 ByRef, Boolean)
# 1:: Int32 AddItemStacked(Int32, Int32, Int32, Int32 ByRef)
# 2:: Int32 AddItemFiltered(Int32, Int32, Int32, Int32 ByRef, Boolean)
# 3:: Int32 AddItemFilteredBanOnly(Int32, Int32, Int32, Int32 ByRef)
# 4:: Int32 AddItem(Int32, Int32, Int32, Int32, Int32, Int32 ByRef)
# 5:: Int32 AddItemBanGridFirst(Int32, Int32, Int32, Int32 ByRef)

# // 参考 [C#][HarmonyPatch]Manual patch internal class/anonymous method/d
# // 参考 https://www.bilibili.com/read/cv22698875/
# // 参考 https://github.com/pardeike/Harmony/issues/393 ， Neutron3529 commented on May 1, 2021
# // 参考 https://github.com/pardeike/Harmony/issues/393#issuecomment-830340953