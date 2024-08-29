import System
from HarmonyLib import Harmony, AccessTools, HarmonyMethod, Traverse
from System.Reflection import Assembly, AssemblyName, TypeAttributes, FieldAttributes, MethodAttributes, CallingConventions, PropertyAttributes, ParameterAttributes
from System.Reflection.Emit import AssemblyBuilderAccess, AssemblyBuilder, ModuleBuilder, TypeBuilder, FieldBuilder, MethodBuilder, PropertyBuilder, ConstructorBuilder, ILGenerator, OpCodes, ParameterBuilder, LocalBuilder


### 原函数的函数参数中有1个或多个ref参数，本脚本无法自动处理，请您手动处理


GUID = "cn.zhufile.dsp.zhu_python3_mod"
harmony = Harmony(GUID)


程序集名称 = "Zhu测试函数"
程序集 = System.AppDomain.CurrentDomain.DefineDynamicAssembly(AssemblyName(程序集名称), AssemblyBuilderAccess.RunAndSave)
模块 = 程序集.DefineDynamicModule(程序集名称, 程序集名称 + ".dll")

def 保存程序集():
    程序集.Save(程序集名称 + ".dll")
    print(f"保存程序集：{程序集名称}.dll")


类型列表 = []
类型名称列表 = []


def HarmonyPatchDefaultPrefix(dsptype, targetname:str, prefixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    函数 = 新建前置函数默认(dsptype, targetname, prefixfunc)
    修补前置(原函数, 函数)


def HarmonyPatchDefaultPostfix(dsptype, targetname:str, postfixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    函数 = 新建后置函数默认(dsptype, targetname, postfixfunc)
    修补后置(原函数, 函数)

def HarmonyPatchDefaultPrefixAndPostfix(dsptype, targetname:str, prefixfunc=None, postfixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    前置函数 = 新建前置函数默认(dsptype, targetname, prefixfunc)
    后置函数 = 新建后置函数默认(dsptype, targetname, postfixfunc)
    修补前置后置(原函数, 前置函数, 后置函数)


def HarmonyPatchDefaultOriginalAndPrefix(dsptype, targetname:str, 原函数=None, prefixfunc=None):
    函数 = 新建前置函数默认(dsptype, targetname, prefixfunc)
    修补前置(原函数, 函数)


def HarmonyPatchDefaultOriginalAndPostfix(dsptype, targetname:str, 原函数=None, postfixfunc=None):
    函数 = 新建后置函数默认(dsptype, targetname, postfixfunc)
    修补后置(原函数, 函数)

def HarmonyPatchDefaultOriginalAndPrefixAndPostfix(dsptype, targetname:str, 原函数=None, prefixfunc=None, postfixfunc=None):
    前置函数 = 新建前置函数默认(dsptype, targetname, prefixfunc)
    后置函数 = 新建后置函数默认(dsptype, targetname, postfixfunc)
    修补前置后置(原函数, 前置函数, 后置函数)



def HarmonyPatchParameterPrefix(dsptype, targetname:str, parastype=[], prefixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname, parastype)
    函数 = 新建前置函数参数(原函数, dsptype, targetname, parastype, prefixfunc)
    修补前置(原函数, 函数)


def HarmonyPatchParameterPostfix(dsptype, targetname:str, parastype=[], postfixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname, parastype)
    函数 = 新建后置函数参数(原函数, dsptype, targetname, parastype, postfixfunc)
    修补后置(原函数, 函数)

def HarmonyPatchParameterPrefixAndPostfix(dsptype, targetname:str, parastype=[], prefixfunc=None, postfixfunc=None):
    原函数 = AccessTools.Method(dsptype, targetname, parastype)
    前置函数 = 新建前置函数参数(原函数, dsptype, targetname, parastype, prefixfunc)
    后置函数 = 新建后置函数参数(原函数, dsptype, targetname, parastype, postfixfunc)
    修补前置后置(原函数, 前置函数, 后置函数)











def HarmonyPatchDefaultPrefixWithReturn(dsptype, targetname:str, returntype=System.Object, funcreturn=None, booleantype=System.Boolean, funcboolean=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    函数 = 新建前置函数默认With返回值(dsptype, targetname, returntype, funcreturn, booleantype, funcboolean)
    修补前置(原函数, 函数)



def HarmonyPatchDefaultPostfixWithReturn(dsptype, targetname:str, returntype=System.Object, funcreturn=None):
    原函数 = AccessTools.Method(dsptype, targetname)
    函数 = 新建后置函数默认With返回值(dsptype, targetname, returntype, funcreturn)
    修补后置(原函数, 函数)




def HarmonyPatchParameterPrefixWithReturn(dsptype, targetname:str, returntype=System.Object, parastype=[], funcreturn=None, booleantype=System.Boolean, funcboolean=None):
    原函数 = AccessTools.Method(dsptype, targetname, parastype) # Boolean RemoveBasePit(Int32)
    函数 = 新建前置函数参数With返回值(原函数, dsptype, targetname, returntype, parastype, funcreturn, booleantype, funcboolean)
    修补前置(原函数, 函数)

def HarmonyPatchParameterPostfixWithReturn(dsptype, targetname:str, returntype=System.Object, parastype=[], funcreturn=None):
    原函数 = AccessTools.Method(dsptype, targetname, parastype) # Boolean RemoveBasePit(Int32)
    函数 = 新建后置函数参数With返回值(原函数, dsptype, targetname, returntype, parastype, funcreturn)
    修补后置(原函数, 函数)



def 新建前置函数默认(dsptype, targetname:str, prefixfunc=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Prefix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    代理 = System.Func[dsptype, System.Boolean]
    字段 = 类型.DefineField("funcBoolean", 代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Boolean, [dsptype]) 
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")

    IL = 方法.GetILGenerator()
    IL.Emit(OpCodes.Ldsfld, 字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(代理, "Invoke"))
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    Traverse.Create(classType).Field("funcBoolean").SetValue( 代理(prefixfunc) )
    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")


def 新建后置函数默认(dsptype, targetname:str, postfixfunc=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Postfix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    代理 = System.Action[dsptype]
    字段 = 类型.DefineField("action", 代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public| MethodAttributes.Static, System.Void, [dsptype]) 
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance") # ParameterAttributes.None
    IL = 方法.GetILGenerator()
    IL.Emit(OpCodes.Ldsfld, 字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(代理, "Invoke"))
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    Traverse.Create(classType).Field("action").SetValue( 代理(postfixfunc) )
    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")


def 新建前置函数默认With返回值(dsptype, targetname:str, returntype=System.Object, funcreturn=None, booleantype=System.Boolean, funcboolean=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Prefix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    返回代理 = System.Func[dsptype, returntype]
    布尔代理 = System.Func[dsptype, System.Boolean]

    返回字段 = 类型.DefineField("funcReturn", 返回代理, FieldAttributes.Public| FieldAttributes.Static) 
    布尔字段 = 类型.DefineField("funcBoolean", 布尔代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Boolean, [dsptype, Ref类型(returntype)]) 

    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")
    方法.DefineParameter(2, getattr(ParameterAttributes, "None"), "__result")

    IL = 方法.GetILGenerator()
    
    IL.Emit(OpCodes.Ldarg_1)
    IL.Emit(OpCodes.Ldsfld, 返回字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(返回代理, "Invoke"))
    Ref_Result_返回值类型赋值(IL, returntype)

    IL.Emit(OpCodes.Ldsfld, 布尔字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(布尔代理, "Invoke"))

    IL.Emit(OpCodes.Ret)
    
    classType = 类型.CreateType()
    
    Traverse.Create(classType).Field("funcReturn").SetValue( 返回代理(funcreturn) )
    Traverse.Create(classType).Field("funcBoolean").SetValue( 布尔代理(funcboolean) )

    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")


def 新建后置函数默认With返回值(dsptype, targetname:str, returntype=System.Object, funcreturn=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Postfix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    返回代理 = System.Func[dsptype, returntype, returntype]
    返回字段 = 类型.DefineField("funcReturn",  返回代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Void, [dsptype, Ref类型(returntype)]) 

    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")
    方法.DefineParameter(2, getattr(ParameterAttributes, "None"), "__result")

    IL = 方法.GetILGenerator()
    
    result = IL.DeclareLocal(returntype) 

    IL.Emit(OpCodes.Ldarg_1)
    Ref_Result_返回值类型读取(IL, returntype)
    IL.Emit(OpCodes.Stloc, result)

    IL.Emit(OpCodes.Ldarg_1)
    IL.Emit(OpCodes.Ldsfld, 返回字段)
    IL.Emit(OpCodes.Ldarg_0)
    IL.Emit(OpCodes.Ldloc_0)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(返回代理, "Invoke"))
    Ref_Result_返回值类型赋值(IL, returntype)

    IL.Emit(OpCodes.Ret)
    
    classType = 类型.CreateType()
    
    Traverse.Create(classType).Field("funcReturn").SetValue( 返回代理(funcreturn) )

    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")


def Ref_Result_返回值类型读取(IL, systemType):
    match systemType:
        case System.Int32: IL.Emit(OpCodes.Ldind_I4)
        case System.UInt32: IL.Emit(OpCodes.Ldind_U4) 
        case System.Boolean: IL.Emit(OpCodes.Ldind_I1)
        case System.Single: IL.Emit(OpCodes.Ldind_R4)
        case _: raise ValueError(f"{systemType} 的代码还没加上 ... ")


def Ref_Result_返回值类型赋值(IL, systemType):
    match systemType:
        case System.Int32: IL.Emit(OpCodes.Stind_I4)
        case System.UInt32: IL.Emit(OpCodes.Stind_I4) # type object 'OpCodes' has no attribute 'Stind_U4'
        case System.Boolean: IL.Emit(OpCodes.Stind_I1)
        case System.Single: IL.Emit(OpCodes.Stind_R4)
        case _: raise ValueError(f"{systemType} 的代码还没加上 ... ")



def 新建前置函数参数(原函数, dsptype, targetname:str, parastype=[], funcprefix=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Prefix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")


    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    布尔参数类型列表 = [dsptype] + parastype + [System.Boolean]
    布尔代理 = System.Func[*布尔参数类型列表]
    布尔字段 = 类型.DefineField("funcBoolean", 布尔代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Boolean, [dsptype] + parastype) 

    参数名称列表 = [parameter.Name for parameter in 原函数.GetParameters()]
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")
    count = 1
    for name in 参数名称列表: 
        count += 1
        方法.DefineParameter(count, getattr(ParameterAttributes, "None"), name)

    IL = 方法.GetILGenerator()
    
    IL.Emit(OpCodes.Ldsfld, 布尔字段)
    IL.Emit(OpCodes.Ldarg_0)
    count = 0
    for name in 参数名称列表: 
        count += 1
        IL.Emit(OpCodes.Ldarg, count)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(布尔代理, "Invoke"))

    IL.Emit(OpCodes.Ret)
    
    classType = 类型.CreateType()
    
    Traverse.Create(classType).Field("funcBoolean").SetValue( 布尔代理(funcprefix) )

    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")



def 新建后置函数参数(原函数, dsptype, targetname:str, parastype=[], funcpostfix=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Postfix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    参数类型列表 = [dsptype] + parastype
    代理 = System.Action[*参数类型列表]
    字段 = 类型.DefineField("action",  代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Void, 参数类型列表) 

    参数名称列表 = [parameter.Name for parameter in 原函数.GetParameters()]
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")
    count = 1
    for name in 参数名称列表: 
        count += 1
        方法.DefineParameter(count, getattr(ParameterAttributes, "None"), name)

    IL = 方法.GetILGenerator()
    
    IL.Emit(OpCodes.Ldsfld, 字段)
    IL.Emit(OpCodes.Ldarg_0)
    count = 0
    for name in 参数名称列表: 
        count += 1
        IL.Emit(OpCodes.Ldarg, count)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(代理, "Invoke"))

    IL.Emit(OpCodes.Ret)
    
    classType = 类型.CreateType()
    
    Traverse.Create(classType).Field("action").SetValue( 代理(funcpostfix) )

    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")








def 新建前置函数参数With返回值(原函数, dsptype, targetname:str, returntype=System.Object, parastype=[], funcreturn=None, booleantype=System.Boolean, funcboolean=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Prefix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    返回参数类型列表 = [dsptype] + parastype + [returntype]
    布尔参数类型列表 = [dsptype] + parastype + [System.Boolean]

    返回代理 = System.Func[*返回参数类型列表]
    布尔代理 = System.Func[*布尔参数类型列表]
    返回字段 = 类型.DefineField("funcReturn", 返回代理, FieldAttributes.Public| FieldAttributes.Static) 
    布尔字段 = 类型.DefineField("funcBoolean", 布尔代理, FieldAttributes.Public| FieldAttributes.Static) 

    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Boolean, [dsptype] + parastype + [Ref类型(returntype)]) 

    参数名称列表 = [parameter.Name for parameter in 原函数.GetParameters()]
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")
    count = 1
    for name in 参数名称列表: 
        count += 1
        方法.DefineParameter(count, getattr(ParameterAttributes, "None"), name)
    count += 1
    方法.DefineParameter(count, getattr(ParameterAttributes, "None"), "__result")

    IL = 方法.GetILGenerator()
    
    IL.Emit(OpCodes.Ldarg, count-1)
    IL.Emit(OpCodes.Ldsfld, 返回字段)
    IL.Emit(OpCodes.Ldarg_0)
    count = 0
    for name in 参数名称列表: 
        count += 1
        IL.Emit(OpCodes.Ldarg, count)

    IL.Emit(OpCodes.Callvirt, AccessTools.Method(返回代理, "Invoke"))
    Ref_Result_返回值类型赋值(IL, returntype)

    IL.Emit(OpCodes.Ldsfld, 布尔字段)
    IL.Emit(OpCodes.Ldarg_0)
    count = 0
    for name in 参数名称列表: 
        count += 1
        IL.Emit(OpCodes.Ldarg, count)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(布尔代理, "Invoke"))

    IL.Emit(OpCodes.Ret)
    
    classType = 类型.CreateType()
    
    Traverse.Create(classType).Field("funcReturn").SetValue( 返回代理(funcreturn) )
    Traverse.Create(classType).Field("funcBoolean").SetValue( 布尔代理(funcboolean) )

    类型列表.append(classType)
    类型名称列表.append(类型名称)
    return AccessTools.Method(classType, "函数")



def 新建后置函数参数With返回值(原函数, dsptype, targetname:str, returntype=System.Object, parastype=[], funcreturn=None):
    类型名称 = f"{dsptype}"[9:-2]
    类型名称 = f"{类型名称}_{targetname}_Postfix"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)

    返回参数类型列表 = [dsptype] + parastype + [returntype, returntype]
    返回代理 = System.Func[*返回参数类型列表]
    返回字段 = 类型.DefineField("funcReturn", 返回代理, FieldAttributes.Public| FieldAttributes.Static) 


    方法 = 类型.DefineMethod("函数", MethodAttributes.Public|MethodAttributes.Static, System.Void, [dsptype] + parastype + [Ref类型(returntype)]) 

    参数名称列表 = [parameter.Name for parameter in 原函数.GetParameters()]
    方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance")
    count = 1
    for name in 参数名称列表: 
        count += 1
        方法.DefineParameter(count, getattr(ParameterAttributes, "None"), name)
    count += 1
    方法.DefineParameter(count, getattr(ParameterAttributes, "None"), "__result")

    IL = 方法.GetILGenerator()

    result = IL.DeclareLocal(returntype) 

    IL.Emit(OpCodes.Ldarg, count-1)
    Ref_Result_返回值类型读取(IL, returntype)
    IL.Emit(OpCodes.Stloc, result)

    IL.Emit(OpCodes.Ldarg, count-1)
    IL.Emit(OpCodes.Ldsfld, 返回字段)
    IL.Emit(OpCodes.Ldarg_0)
    count = 0
    for name in 参数名称列表: 
        count += 1
        IL.Emit(OpCodes.Ldarg, count)
    IL.Emit(OpCodes.Ldloc, result)
    IL.Emit(OpCodes.Callvirt, AccessTools.Method(返回代理, "Invoke"))
    Ref_Result_返回值类型赋值(IL, returntype)


    IL.Emit(OpCodes.Ret)
    
    classType = 类型.CreateType()
    
    Traverse.Create(classType).Field("funcReturn").SetValue( 返回代理(funcreturn) )

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




def 系统类型(dsptype):
    类型名称 = f"{dsptype}"[8:-2] # <class 'System.Int32'>
    systemType = System.Type.GetType(类型名称) 
    return systemType


def Ref类型(dsptype):
    类型名称 = f"{dsptype}"[8:-2] # <class 'System.Int32'>
    systemType = System.Type.GetType(类型名称) 
    return systemType.MakeByRefType()