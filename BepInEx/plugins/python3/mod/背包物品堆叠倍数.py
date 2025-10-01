import System

from dsptype import StorageComponent, LDB, GameMain
from dspharmony import HarmonyPatch_Prefix_Default, HarmonyPatch_Postfix_Default, HarmonyPatch_Static_Postfix_Default




def Start():

    HarmonyPatch_Static_Postfix_Default(StorageComponent, "LoadStatic", postfunc=Postfix) # static void LoadStatic()

    HarmonyPatch_Prefix_Default(StorageComponent, "Sort", prefunc=StoragePrefix) # void Sort(bool raiseNotify = true)
    HarmonyPatch_Postfix_Default(StorageComponent, "Sort", postfunc=StoragePostfix)

    HarmonyPatch_Prefix_Default(StorageComponent, "AddItemStacked", prefunc=StoragePrefix) # int AddItemStacked(int itemId, int count, int inc, out int remainInc)
    HarmonyPatch_Postfix_Default(StorageComponent, "AddItemStacked", postfunc=StoragePostfix)

    类型列表 = [System.Int32, System.Int32, System.Int32, System.Int32, System.Int32, System.Type.GetType("System.Int32").MakeByRefType()]
    HarmonyPatch_Prefix_Default(StorageComponent, "AddItem", parastype=类型列表, prefunc=StoragePrefix)
    HarmonyPatch_Postfix_Default(StorageComponent, "AddItem", parastype=类型列表, postfunc=StoragePostfix) # int AddItem( int itemId, int count, int startIndex, int length, int inc, out int remainInc)





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



def StoragePrefix(__instance, *args, **kwargs):
    if __instance == GameMain.data.mainPlayer.package: StorageComponent.itemStackCount = newitemStackCount
    return True

def StoragePostfix(__instance, *args, **kwargs):
    if __instance == GameMain.data.mainPlayer.package: StorageComponent.itemStackCount = olditemStackCount

# print(dir(System.Int32))
# ['CompareTo', 'Equals', 'Finalize', 'GetHashCode', 'GetType', 'GetTypeCode', 'MaxValue', 'MemberwiseClone', 'MinValue', 'Overloads', 'Parse', 'ReferenceEquals', 
#  'ToString', 'TryParse', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__float__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', 
#  '__hash__', '__index__', '__init__', '__init_subclass__', '__int__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__overloads__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']


# print([System.Int32, System.Type.GetType("System.Int32")]) # [<class 'System.Int32'>, <System.RuntimeType object at 0x00000292BCEFED80>]


# from dspassembly import 程序集类型
# dspAssemblyType = 程序集类型(".\\DSPGAME_Data\\Managed\\Assembly-CSharp.dll", "StorageComponent")
# def AddItem():
#     # dspAssemblyType.PrintMethod("AddItem")
#     return dspAssemblyType.FindMethod("AddItem")[4]

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