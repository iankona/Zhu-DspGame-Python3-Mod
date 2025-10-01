import System
import UnityEngine
import types
from dspassembly import 程序集类型





assemblyType = 程序集类型(".\\BepInEx\\plugins\\Python3Mod\\modmanage\\ZhuMoMo类型.dll", "ZhuMoMoStart")
def 实例MonoBehaviour类(funcstart=None, funcupdate=None, funcongui=None): # type() == types.FunctionType, callable()判断对象能否被调用
    实例 = None
    match [type(funcstart), type(funcupdate), type(funcongui)]:
        case [types.FunctionType, types.NoneType, types.NoneType]: 
            类型 = assemblyType.SetType("ZhuMoMoStart")
            print(类型)
            实例 = System.Activator.CreateInstance(类型)
            # 实例 = UnityEngine.Object.Instantiate[类型]()
            print(实例)
            print(实例.actionStart)
            实例.actionStart = System.Action[类型](funcstart)
            实例.Start()

    match [type(funcstart), type(funcupdate), type(funcongui)]:
        case [types.NoneType, types.FunctionType, types.NoneType]: 
            类型 = assemblyType.SetType("ZhuMoMoUpdate")
            print(类型)
            脚本 = System.Activator.CreateInstance(类型)
            # 实例 = UnityEngine.Object.Instantiate[类型]()
            print(脚本)
            print(脚本.actionUpdate)
            脚本.actionUpdate = System.Action[类型](funcupdate)

