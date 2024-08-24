import System
from HarmonyLib import Harmony, AccessTools, HarmonyMethod, Traverse
from System.Reflection import Assembly, AssemblyName, TypeAttributes, FieldAttributes, MethodAttributes, CallingConventions, PropertyAttributes, ParameterAttributes
from System.Reflection.Emit import AssemblyBuilderAccess, AssemblyBuilder, ModuleBuilder, TypeBuilder, FieldBuilder, MethodBuilder, PropertyBuilder, ConstructorBuilder, ILGenerator, OpCodes, ParameterBuilder, LocalBuilder


GUID = "cn.zhufile.dsp.zhu_python3_mod"
harmony = Harmony(GUID)


程序集名称 = "Zhu测试函数"
程序集 = System.AppDomain.CurrentDomain.DefineDynamicAssembly(AssemblyName(程序集名称), AssemblyBuilderAccess.RunAndSave)
模块 = 程序集.DefineDynamicModule(程序集名称, 程序集名称 + ".dll")

def 保存程序集():
    程序集.Save(程序集名称 + ".dll")


类型列表 = []
类型名称列表 = []


def HarmonyPatchDefaultPrefix(dsptype, targetname:str, prefixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    前置函数 = 新建前置函数默认(dsptype, targetname, prefixfunc)
    修补前置(原函数, 前置函数)


def HarmonyPatchDefaultPostfix(dsptype, targetname:str, postfixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    后置函数 = 新建后置函数默认(dsptype, targetname, postfixfunc)
    修补后置(原函数, 后置函数)

def HarmonyPatchDefaultPrefixAndPostfix(dsptype, targetname:str, prefixfunc=None, postfixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    前置函数 = 新建前置函数默认(dsptype, targetname, prefixfunc)
    后置函数 = 新建后置函数默认(dsptype, targetname, postfixfunc)
    修补前置后置(原函数, 前置函数, 后置函数)




def 新建前置函数默认(dsptype, targetname:str, prefixfunc=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Prefix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    字段名称 = f"func{targetname}Prefix"
    前置字段 = 类型.DefineField(字段名称,  System.Func[dsptype, System.Boolean], FieldAttributes.Public| FieldAttributes.Static) 

    前置方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Boolean, [dsptype]) 
    前置方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")
    IL = 前置方法.GetILGenerator()
    IL.Emit(OpCodes.Ldsfld, 前置字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(System.Func[dsptype, System.Boolean], "Invoke"))
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    Traverse.Create(classType).Field(字段名称).SetValue(System.Func[dsptype, System.Boolean](prefixfunc))
    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")


def 新建后置函数默认(dsptype, targetname:str, postfixfunc=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Postfix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    字段名称 = f"action{targetname}Postfix"
    后置字段 = 类型.DefineField(字段名称, System.Action[dsptype], FieldAttributes.Public| FieldAttributes.Static) 

    后置方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Void, [dsptype]) 
    后置方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance") # ParameterAttributes.None
    IL = 后置方法.GetILGenerator()
    IL.Emit(OpCodes.Ldsfld, 后置字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(System.Action[dsptype], "Invoke"))
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    Traverse.Create(classType).Field(字段名称).SetValue(System.Action[dsptype](postfixfunc))
    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")




def 修补前置(原函数, 前置函数):
    patchProcessor = harmony.CreateProcessor(原函数)
    patchProcessor.AddPrefix(HarmonyMethod(前置函数))
    patchProcessor.Patch()



def 修补后置(原函数, 后置函数):
    patchProcessor = harmony.CreateProcessor(原函数)
    patchProcessor.AddPostfix(HarmonyMethod(后置函数))
    patchProcessor.Patch()


def 修补前置后置(原函数, 前置函数, 后置函数):
    patchProcessor = harmony.CreateProcessor(原函数)
    patchProcessor.AddPrefix(HarmonyMethod(前置函数))
    patchProcessor.AddPostfix(HarmonyMethod(后置函数))
    # patchProcessor.AddTranspiler(transpiler)
    # patchProcessor.AddFinalizer(finalizer)
    # patchProcessor.AddILManipulator(ilmanipulator)
    patchProcessor.Patch()






