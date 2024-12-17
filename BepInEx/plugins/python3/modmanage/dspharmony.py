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


def HarmonyPatch_Prefix_Default(dsptype, targetname:str, parastype=[], prefunc=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Prefix")
    参数名称列表, 参数类型列表 = ["__instance"]+[parameter.Name for parameter in 原函数.GetParameters()], [dsptype]+[parameter.ParameterType for parameter in 原函数.GetParameters()] 

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Boolean, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()


    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Func[*代理定义列表, System.Boolean]
    字段名称 = "funcBool"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue(代理(prefunc))
    修补前置(原函数, AccessTools.Method(classType, 方法名称))




def HarmonyPatch_Prefix_Result(dsptype, targetname:str, parastype=[], preresult=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Prefix")
    参数名称列表, 参数类型列表 = ["__instance"]+[parameter.Name for parameter in 原函数.GetParameters()]+["__result"], [dsptype]+[parameter.ParameterType for parameter in 原函数.GetParameters()]+[原函数.ReturnType.MakeByRefType()]

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Boolean, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Func[*代理定义列表, 原函数.ReturnType]
    字段名称 = "funcResult"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    IL.Emit(OpCodes.Ldarg, len(参数类型列表)-1)
    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes_Stind(原函数.ReturnType))

    # 默认为假，拦截原函数
    IL.Emit(OpCodes.Ldc_I4_0)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue( 代理(preresult) )
    修补前置(原函数, AccessTools.Method(classType, 方法名称))



def HarmonyPatch_Prefix_DefaultAndResult(dsptype, targetname:str, parastype=[], prefunc=None, preresult=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Prefix")
    参数名称列表, 参数类型列表 = ["__instance"]+[parameter.Name for parameter in 原函数.GetParameters()]+["__result"], [dsptype]+[parameter.ParameterType for parameter in 原函数.GetParameters()]+[原函数.ReturnType.MakeByRefType()]

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Boolean, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理1 = System.Func[*代理定义列表, System.Boolean]
    代理2 = System.Func[*代理定义列表, 原函数.ReturnType]

    字段名称1 = "funcBool"
    字段名称2 = "funcResult"

    字段1 = 类型.DefineField(字段名称1, 代理1, FieldAttributes.Public| FieldAttributes.Static) 
    字段2 = 类型.DefineField(字段名称2, 代理2, FieldAttributes.Public| FieldAttributes.Static) 

    IL.Emit(OpCodes.Ldarg, len(参数类型列表)-1)
    委托函数体(IL, 代理2, 字段2, 参数类型列表)
    IL.Emit(OpCodes_Stind(原函数.ReturnType))

    委托函数体(IL, 代理1, 字段1, 参数类型列表)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称1).SetValue( 代理1(prefunc) )
    Traverse.Create(classType).Field(字段名称2).SetValue( 代理2(preresult) )
    修补前置(原函数, AccessTools.Method(classType, 方法名称))






def HarmonyPatch_Postfix_Default(dsptype, targetname:str, parastype=[], postfunc=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Postfix")
    参数名称列表, 参数类型列表 = ["__instance"]+[parameter.Name for parameter in 原函数.GetParameters()], [dsptype]+[parameter.ParameterType for parameter in 原函数.GetParameters()] 

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Void, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Action[*代理定义列表]
    字段名称 = "actionVoid"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue(代理(postfunc))
    修补后置(原函数, AccessTools.Method(classType, 方法名称))



def HarmonyPatch_Postfix_Result(dsptype, targetname:str, parastype=[], postresult=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Postfix")
    参数名称列表, 参数类型列表 = ["__instance"]+[parameter.Name for parameter in 原函数.GetParameters()]+["__result"], [dsptype]+[parameter.ParameterType for parameter in 原函数.GetParameters()]+[原函数.ReturnType.MakeByRefType()]

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Void, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Func[*代理定义列表, 原函数.ReturnType]
    字段名称 = "funcResult"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    IL.Emit(OpCodes.Ldarg, len(参数类型列表)-1)
    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes_Stind(原函数.ReturnType))

    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue( 代理(postresult) )
    修补后置(原函数, AccessTools.Method(classType, 方法名称))




### 修改静态方法需要删除 ["__instance"] 和 [dsptype]




def HarmonyPatch_Static_Prefix_Default(dsptype, targetname:str, parastype=[], prefunc=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Prefix")
    参数名称列表, 参数类型列表 = [parameter.Name for parameter in 原函数.GetParameters()], [parameter.ParameterType for parameter in 原函数.GetParameters()] 
    if 参数名称列表 == []: 参数名称列表, 参数类型列表 = ["__instance"], [dsptype] # System.System.Action, does not accept 0 generic parameters

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Boolean, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()


    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Func[*代理定义列表, System.Boolean]
    字段名称 = "funcBool"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue(代理(prefunc))
    修补前置(原函数, AccessTools.Method(classType, 方法名称))




def HarmonyPatch_Static_Prefix_Result(dsptype, targetname:str, parastype=[], preresult=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Prefix")
    参数名称列表, 参数类型列表 = [parameter.Name for parameter in 原函数.GetParameters()]+["__result"], [parameter.ParameterType for parameter in 原函数.GetParameters()]+[原函数.ReturnType.MakeByRefType()]

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Boolean, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Func[*代理定义列表, 原函数.ReturnType]
    字段名称 = "funcResult"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    IL.Emit(OpCodes.Ldarg, len(参数类型列表)-1)
    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes_Stind(原函数.ReturnType))

    # 默认为假，拦截原函数
    IL.Emit(OpCodes.Ldc_I4_0)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue( 代理(preresult) )
    修补前置(原函数, AccessTools.Method(classType, 方法名称))



def HarmonyPatch_Static_Prefix_DefaultAndResult(dsptype, targetname:str, parastype=[], prefunc=None, preresult=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Prefix")
    参数名称列表, 参数类型列表 = [parameter.Name for parameter in 原函数.GetParameters()]+["__result"], [parameter.ParameterType for parameter in 原函数.GetParameters()]+[原函数.ReturnType.MakeByRefType()]

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Boolean, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理1 = System.Func[*代理定义列表, System.Boolean]
    代理2 = System.Func[*代理定义列表, 原函数.ReturnType]

    字段名称1 = "funcBool"
    字段名称2 = "funcResult"

    字段1 = 类型.DefineField(字段名称1, 代理1, FieldAttributes.Public| FieldAttributes.Static) 
    字段2 = 类型.DefineField(字段名称2, 代理2, FieldAttributes.Public| FieldAttributes.Static) 

    IL.Emit(OpCodes.Ldarg, len(参数类型列表)-1)
    委托函数体(IL, 代理2, 字段2, 参数类型列表)
    IL.Emit(OpCodes_Stind(原函数.ReturnType))

    委托函数体(IL, 代理1, 字段1, 参数类型列表)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称1).SetValue( 代理1(prefunc) )
    Traverse.Create(classType).Field(字段名称2).SetValue( 代理2(preresult) )
    修补前置(原函数, AccessTools.Method(classType, 方法名称))




# Func最少接受0个输入1个输出
# Action接受1~16个参数
def HarmonyPatch_Static_Postfix_Default(dsptype, targetname:str, parastype=[], postfunc=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Postfix")
    参数名称列表, 参数类型列表 = [parameter.Name for parameter in 原函数.GetParameters()], [parameter.ParameterType for parameter in 原函数.GetParameters()] 
    if 参数名称列表 == []: 参数名称列表, 参数类型列表 = ["__instance"], [dsptype] # System.System.Action, does not accept 0 generic parameters

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Void, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Action[*代理定义列表]
    字段名称 = "actionVoid"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue(代理(postfunc))
    修补后置(原函数, AccessTools.Method(classType, 方法名称))



def HarmonyPatch_Static_Postfix_Result(dsptype, targetname:str, parastype=[], postresult=None):
    原函数 = 查找原函数(dsptype, targetname, parastype)
    类型名称 = 类型名称检查(dsptype, targetname, "Postfix")
    参数名称列表, 参数类型列表 = [parameter.Name for parameter in 原函数.GetParameters()]+["__result"], [parameter.ParameterType for parameter in 原函数.GetParameters()]+[原函数.ReturnType.MakeByRefType()]

    类型 = 模块.DefineType(类型名称, TypeAttributes.Public)
    方法名称 = "函数"
    方法 = 类型.DefineMethod(方法名称, MethodAttributes.Public|MethodAttributes.Static, System.Void, 参数类型列表) 
    for i, paraname in enumerate(参数名称列表): 
        方法.DefineParameter(i+1, getattr(ParameterAttributes, "None"), paraname)
    IL = 方法.GetILGenerator()

    代理定义列表 = 代理参数处理(参数类型列表)
    代理 = System.Func[*代理定义列表, 原函数.ReturnType]
    字段名称 = "funcResult"
    字段 = 类型.DefineField(字段名称, 代理, FieldAttributes.Public| FieldAttributes.Static) 

    IL.Emit(OpCodes.Ldarg, len(参数类型列表)-1)
    委托函数体(IL, 代理, 字段, 参数类型列表)
    IL.Emit(OpCodes_Stind(原函数.ReturnType))

    IL.Emit(OpCodes.Ret)

    classType = 类型.CreateType()
    类型列表.append(classType)
    Traverse.Create(classType).Field(字段名称).SetValue( 代理(postresult) )
    修补后置(原函数, AccessTools.Method(classType, 方法名称))



# def HarmonyPatch_PrefixAndPostfix_Default(dsptype, targetname:str, parastype=[], prefunc=None, postfunc=None):
#     HarmonyPatch_Prefix_Default(dsptype, targetname, parastype, prefunc)
#     HarmonyPatch_Postfix_Default(dsptype, targetname, parastype, postfunc)



def 查找原函数(dsptype, targetname:str, parastype=[]):
    # print([dsptype, targetname])
    if parastype == []:
        原函数 = AccessTools.Method(dsptype, targetname)
    else:
        原函数 = AccessTools.Method(dsptype, targetname, parastype)
    # print([dsptype, targetname, 原函数])
    return 原函数


def 类型名称检查(dsptype, targetname:str, suffix:str):
    classname = f"{dsptype}"[9:-2]
    类型名称 = f"{classname}_{targetname}_{suffix}"
    if 类型名称 in 类型名称列表: raise ValueError(f"{类型名称}: 命名冲突，请检查是否和其他mod(Python模块)函数修改冲突")
    类型名称列表.append(类型名称)
    return 类型名称



def OpCodes_Ldind(paratype):
    classname = f"{paratype}"
    if classname.startswith("<class"): classname = classname[8:-2]
    if classname.startswith("."): classname = classname[1:]

    match classname:
        case "System.Boolean": return OpCodes.Ldind_I1
        case "System.Int32": return OpCodes.Ldind_I4
        case "System.UInt32": return OpCodes.Ldind_U4
        case "System.Single": return OpCodes.Ldind_R4

    if "[]" in classname: return OpCodes.Ldind_Ref
    else:
        raise ValueError(f"{classname} 的代码还没加上 ... ")
    

def OpCodes_Stind(paratype):
    classname = f"{paratype}"
    if classname.startswith("<class"): classname = classname[8:-2]
    if classname.startswith("."): classname = classname[1:]

    match classname:
        case "System.Boolean": return OpCodes.Stind_I1
        case "System.Int32": return OpCodes.Stind_I4
        case "System.UInt32": return OpCodes.Stind_I4 # type object 'OpCodes' has no attribute 'Stind_U4'
        case "System.Single": return OpCodes.Stind_R4
        
    if "[]" in classname: return OpCodes.Stind_Ref
    else:
        raise ValueError(f"{classname} 的代码还没加上 ... ")


def 代理参数处理(参数类型列表):
    列表 = []
    for paratype in 参数类型列表: 
        if f"{paratype}".endswith("&"): 
            列表.append( paratype.GetElementType() )
        else:
            列表.append( paratype )
    return 列表


def 委托函数体(IL, 代理, 字段, 参数类型列表):
    IL.Emit(OpCodes.Ldsfld, 字段)
    for i, paratype in enumerate(参数类型列表):
        IL.Emit(OpCodes.Ldarg, i)
        classname = f"{paratype}"
        if classname.endswith("&"): IL.Emit(OpCodes_Ldind(paratype.GetElementType()))
    IL.Emit(OpCodes.Callvirt, AccessTools.Method( 代理, "Invoke") )


# Type.HasElementType
def UnRef处理(paratype):
    classname = f"{paratype}"
    if classname.endswith("&"): return paratype.GetElementType()
    return paratype
    # classname = f"{paratype}"
    # if classname.endswith("&"): 
    #     print([i, paratype.FullName, paratype.GetElementType().FullName])
    # else:
    #     print([i, classname]) # type object 'NearColliderLogic' has no attribute 'Name', "FullName"  

# print([i, f"{paratype}", paratype]) # 直接print与f{}是不一样的
# # [0, "<class '.NearColliderLogic'>", <class '.NearColliderLogic'>]
# # [1, 'UnityEngine.Vector3', <System.RuntimeType object at 0x0000015215D1A000>]
# # [2, 'System.Single&', <System.RuntimeType object at 0x0000015215D19F80>]
# # [3, 'System.Int32[]&', <System.RuntimeType object at 0x0000015215D19FC0>]





def 修补前置(原函数, 前置函数):
    patchProcessor = harmony.CreateProcessor(原函数)
    patchProcessor.AddPrefix(HarmonyMethod(前置函数))
    patchProcessor.Patch()



def 修补后置(原函数, 后置函数):
    patchProcessor = harmony.CreateProcessor(原函数)
    patchProcessor.AddPostfix(HarmonyMethod(后置函数))
    patchProcessor.Patch()



# def 修补前置后置(原函数, 前置函数, 后置函数):
#     patchProcessor = harmony.CreateProcessor(原函数)
#     patchProcessor.AddPrefix(HarmonyMethod(前置函数))
#     patchProcessor.AddPostfix(HarmonyMethod(后置函数))
#     # patchProcessor.AddTranspiler(transpiler)
#     # patchProcessor.AddFinalizer(finalizer)
#     # patchProcessor.AddILManipulator(ilmanipulator)
#     patchProcessor.Patch()


# # 目前通过 parameter.ParameterType for parameter in 原函数.GetParameters() 获取的都是System.RuntimeType, 基本不会遇到手动编写python代码的<class 'System.Single'>
# def 测试():
#     type = System.Single # print(type) # <class 'System.Single'> 和 <System.RuntimeType object at 0x0000015215D1A000> 后续遇到了这个问题在处理，
#     # reftype = System.Single.MakeByRefType() # type object 'Single' has no attribute 'MakeByRefType'
# 测试()




# # System.Int32, int
# # System.Single, float
# # System.Double, double
# # System.Boolean, bool
# # System.Array[System.Int32], int[] 



# # if(methodInfo.ReturnType.Name == "Void"){
# #   // Your Code.........
# # }