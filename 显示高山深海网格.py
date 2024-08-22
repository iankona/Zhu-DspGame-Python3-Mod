import System
from dsptype import UIBuildingGrid, GameMain
from HarmonyLib import AccessTools, HarmonyMethod, Traverse

from System.Reflection import Assembly, AssemblyName, TypeAttributes, FieldAttributes, MethodAttributes, CallingConventions, PropertyAttributes, ParameterAttributes
from System.Reflection.Emit import AssemblyBuilderAccess, AssemblyBuilder, ModuleBuilder, TypeBuilder, FieldBuilder, MethodBuilder, PropertyBuilder, ConstructorBuilder, ILGenerator, OpCodes, ParameterBuilder, LocalBuilder


# import clr
# clr.AddReference("Zhu静态函数")
# from 静态函数 import 生成测试
# # 生成测试.运行()



from HarmonyLib import Harmony



GUID = "cn.zhufile.dsp.zhu_python3_mod"
harmony = Harmony(GUID)
def Start():
    pass
    修补函数()

def Update():
    pass


def OnGUI():
    pass



def 修补函数():
    pass
    原函数 = AccessTools.Method(UIBuildingGrid, "Update")
    prefix = AccessTools.Method(ClassType, "Update"+"Prefix")
    postfix = AccessTools.Method(ClassType, "Update"+"Postfix")

    # print(原函数)
    # print(prefix)
    # print(postfix)
    # harmony.Patch(原函数, HarmonyMethod(prefix), HarmonyMethod(postfix)) 
    # harmony.Patch(原函数, HarmonyMethod(prefix))
    # harmony.Patch(原函数, System.null, HarmonyMethod(postfix)) # 不起作用
    patchProcessor = harmony.CreateProcessor(原函数)
	# patchProcessor.AddPrefix(prefix)
    patchProcessor.AddPostfix(HarmonyMethod(postfix))
	# patchProcessor.AddTranspiler(transpiler)
	# patchProcessor.AddFinalizer(finalizer)
	# patchProcessor.AddILManipulator(ilmanipulator)
    patchProcessor.Patch()

# print(__file__) # D:\Program_disport\Stream\steamapps\common\Dyson Sphere Program\.\BepInEx\plugins\Python3Mod\mod\显示高山深海网格\显示网格.py
# print(__name__)  # 显示高山深海网格.显示网格
# print(__package__) # 显示高山深海网格
# # print(__path__) # name '__path__' is not defined
# # print(__qualname__) # name '__qualname__' is not defined
# print(f"名称：{UIBuildingGrid.name}") # type object 'UIBuildingGrid' has no attribute 'Name'
# # 名称：<property 'System.String name'>
# #动态创建程序集名称  



dllbasename = "Zhu测试函数"
程序集名称 = AssemblyName(dllbasename);  
dynamicAssembly = System.AppDomain.CurrentDomain.DefineDynamicAssembly(程序集名称, AssemblyBuilderAccess.RunAndSave) # AssemblyBuilder
# 动态创建模块  
模块 = dynamicAssembly.DefineDynamicModule(程序集名称.Name, 程序集名称.Name + ".dll") # ModuleBuilder 
# 动态创建类MyClass  
类型 = 模块.DefineType("ZhuUIBuildingGrid", TypeAttributes.Public) # TypeBuilder 

前置字段 = 类型.DefineField("funcUpdatePrefix",  System.Func[UIBuildingGrid, System.Boolean], FieldAttributes.Public| FieldAttributes.Static) # FieldBuilder 
后置字段 = 类型.DefineField("funcUpdatePostfix", System.Func[UIBuildingGrid, System.Boolean], FieldAttributes.Public| FieldAttributes.Static) # FieldBuilder 

前置方法 = 类型.DefineMethod("UpdatePrefix", MethodAttributes.Public|MethodAttributes.Static, System.Boolean, [UIBuildingGrid]) 
前置方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance") # ParameterAttributes.None
前置方法IL = 前置方法.GetILGenerator()
flag = 前置方法IL.DeclareLocal(System.Boolean) # 定义局部变量 # bool flag = true; 变量名称已自动处理好了
labelEnd1   = 前置方法IL.DefineLabel()
前置方法IL.Emit(OpCodes.Ldc_I4_1)# il.Emit(OpCodes.Ldc_I4, 1);
前置方法IL.Emit(OpCodes.Stloc_0) # il.Emit(OpCodes.Stloc, flag)
前置方法IL.Emit(OpCodes.Ldsfld, 前置字段)
前置方法IL.Emit(OpCodes.Brfalse_S, labelEnd1)
前置方法IL.Emit(OpCodes.Ldsfld, 前置字段)
前置方法IL.Emit(OpCodes.Ldarg_0)
前置方法IL.Emit(OpCodes.Callvirt, AccessTools.Method(System.Func[UIBuildingGrid, System.Boolean], "Invoke"))
前置方法IL.Emit(OpCodes.Stloc_0)
前置方法IL.MarkLabel(labelEnd1)
前置方法IL.Emit(OpCodes.Ldloc_0)
前置方法IL.Emit(OpCodes.Ret)

后置方法 = 类型.DefineMethod("UpdatePostfix", MethodAttributes.Public|MethodAttributes.Static, System.Void, [UIBuildingGrid]) 
后置方法.DefineParameter(1, getattr(ParameterAttributes, "None"), "__instance") # ParameterAttributes.None
后置方法IL = 后置方法.GetILGenerator()
labelFalse  = 后置方法IL.DefineLabel()
后置方法IL.Emit(OpCodes.Ldsfld, 后置字段)
后置方法IL.Emit(OpCodes.Brfalse_S, labelFalse)
后置方法IL.Emit(OpCodes.Ldsfld, 后置字段)
后置方法IL.Emit(OpCodes.Ldarg_0)
后置方法IL.Emit(OpCodes.Callvirt, AccessTools.Method(System.Func[UIBuildingGrid, System.Boolean], "Invoke"))
后置方法IL.Emit(OpCodes.Pop)
后置方法IL.MarkLabel(labelFalse)
后置方法IL.Emit(OpCodes.Ret)


# print(dir(前置方法))

# ['AddDeclarativeSecurity', 'Attributes', 'CallingConvention', 'ContainsGenericParameters', 'CreateDelegate', 'CreateMethodBody', 'CustomAttributes', 'DeclaringType', 'DefineGenericParameters', 'DefineParameter', 'Equals', 'Finalize', 'GetBaseDefinition', 'GetCurrentMethod', 'GetCustomAttributes', 'GetCustomAttributesData', 'GetGenericArguments', 'GetGenericMethodDefinition', 'GetHashCode', 'GetILGenerator', 'GetMethodBody', 'GetMethodFromHandle', 'GetMethodImplementationFlags', 'GetModule', 'GetParameters', 'GetToken', 'GetType', 'InitLocals', 'Invoke', 'IsAbstract', 'IsAssembly', 'IsConstructor', 'IsDefined', 'IsFamily', 'IsFamilyAndAssembly', 'IsFamilyOrAssembly', 'IsFinal', 'IsGenericMethod', 'IsGenericMethodDefinition', 'IsHideBySig', 'IsPrivate', 'IsPublic', 'IsSecurityCritical', 'IsSecuritySafeCritical', 'IsSecurityTransparent', 'IsSpecialName', 'IsStatic', 'IsVirtual', 'MakeGenericMethod', 'MemberType', 'MemberwiseClone', 'MetadataToken', 'MethodHandle', 'MethodImplementationFlags', 'Module', 'Name', 'Overloads', 'ReferenceEquals', 'ReflectedType', 'ReturnParameter', 'ReturnType', 'ReturnTypeCustomAttributes', 'SetCustomAttribute', 'SetImplementationFlags', 'SetMarshal', 'SetMethodBody', 'SetParameters', 'SetReturnType', 'SetSignature', 'SetSymCustomAttribute', 'Signature', 'ToString', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__overloads__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'get_Attributes', 'get_CallingConvention', 'get_ContainsGenericParameters', 'get_CustomAttributes', 'get_DeclaringType', 'get_InitLocals', 'get_IsAbstract', 'get_IsAssembly', 'get_IsConstructor', 'get_IsFamily', 'get_IsFamilyAndAssembly', 'get_IsFamilyOrAssembly', 'get_IsFinal', 'get_IsGenericMethod', 'get_IsGenericMethodDefinition', 'get_IsHideBySig', 'get_IsPrivate', 'get_IsPublic', 'get_IsSecurityCritical', 'get_IsSecuritySafeCritical', 'get_IsSecurityTransparent', 'get_IsSpecialName', 'get_IsStatic', 'get_IsVirtual', 'get_MemberType', 'get_MetadataToken', 'get_MethodHandle', 'get_MethodImplementationFlags', 'get_Module', 'get_Name', 'get_ReflectedType', 'get_ReturnParameter', 'get_ReturnType', 'get_ReturnTypeCustomAttributes', 'get_Signature', 'op_Equality', 'op_Inequality', 'set_InitLocals']
# 
# #使用动态类创建类型  
ClassType = 类型.CreateType()
#保存动态创建的程序集名称 (程序集名称将保存在程序目录下调试时就在Debug下)  
# dynamicAssembly.Save(程序集名称.Name + ".dll")
#创建类  
#return classType;  

# print(ClassType)



def Prefix(__instance):
    # print("前置有运行==========")
    return True


def Postfix(__instance):
    # print("==========后置有运行")
    pass

    material = Traverse.Create(__instance).Field("material").GetValue()
    if GameMain.mainPlayer != None:
        material.SetFloat("_ZMin", -8.0)  # Mountains
        material.SetFloat("_ZMax",  8.0)  # Oceans

    return True

# print(ClassType) # ZhuUIBuildingGrid
# print(dir(UIBuildingGrid))
# ['BroadcastMessage', 'CancelInvoke', 'CompareTag', 'Destroy', 'DestroyImmediate', 'DestroyObject', 'DontDestroyOnLoad', 'Equals', 'Finalize', 'FindObjectOfType', 'FindObjectsOfType', 'FindObjectsOfTypeAll', 'FindObjectsOfTypeIncludingAssets', 'FindSceneObjectsOfType', 'FreeReformMap', 'GetComponent', 'GetComponentInChildren', 'GetComponentInParent', 'GetComponents', 'GetComponentsInChildren', 'GetComponentsInParent', 'GetHashCode', 'GetInstanceID', 'GetType', 'InitReformMap', 'Instantiate', 'Invoke', 'InvokeRepeating', 'IsInvoking', 'MemberwiseClone', 'OnGameEnded', 'Overloads', 'ReferenceEquals', 'SendMessage', 'SendMessageUpwards', 'StartCoroutine', 'StartCoroutine_Auto', 'StopAllCoroutines', 'StopCoroutine', 'ToString', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__overloads__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'altGridRnd', 'blueprintColor', 'blueprintGridRnd', 'buildColor', 'dismantleColor', 'downgradeColor', 'enabled', 'gameObject', 'get_enabled', 'get_gameObject', 'get_hideFlags', 'get_isActiveAndEnabled', 'get_name', 'get_tag', 'get_transform', 'get_useGUILayout', 'gridRnd', 'hideFlags', 'isActiveAndEnabled', 'name', 'op_Equality', 'op_Implicit', 'op_Inequality', 'print', 'reformColor', 'reformCursorBuffer', 'set_enabled', 'set_hideFlags', 'set_name', 'set_tag', 'set_useGUILayout', 'tag', 'transform', 'upgradeColor', 'useGUILayout']
# print(dir(ClassType))
# ['AsType', 'Assembly', 'AssemblyQualifiedName', 'Attributes', 'BaseType', 'Clone', 'ContainsGenericParameters', 'CustomAttributes', 'DeclaredConstructors', 'DeclaredEvents', 'DeclaredFields', 'DeclaredMembers', 'DeclaredMethods', 'DeclaredNestedTypes', 'DeclaredProperties', 'DeclaringMethod', 'DeclaringType', 'DefaultBinder', 'Delimiter', 'EmptyTypes', 'Equals', 'FilterAttribute', 'FilterName', 'FilterNameIgnoreCase', 'Finalize', 'FindInterfaces', 'FindMembers', 'FullName', 'GUID', 'GenericParameterAttributes', 'GenericParameterPosition', 'GenericTypeArguments', 'GenericTypeParameters', 'GetArrayRank', 'GetAttributeFlagsImpl', 'GetConstructor', 'GetConstructorImpl', 'GetConstructors', 'GetCustomAttributes', 'GetCustomAttributesData', 'GetDeclaredEvent', 'GetDeclaredField', 'GetDeclaredMethod', 'GetDeclaredMethods', 'GetDeclaredNestedType', 'GetDeclaredProperty', 'GetDefaultMembers', 'GetElementType', 'GetEnumName', 'GetEnumNames', 'GetEnumUnderlyingType', 'GetEnumValues', 'GetEvent', 'GetEvents', 'GetField', 'GetFields', 'GetGenericArguments', 'GetGenericParameterConstraints', 'GetGenericTypeDefinition', 'GetHashCode', 'GetInterface', 'GetInterfaceMap', 'GetInterfaces', 'GetMember', 'GetMembers', 'GetMethod', 'GetMethodImpl', 'GetMethods', 'GetNestedType', 'GetNestedTypes', 'GetObjectData', 'GetProperties', 'GetProperty', 'GetPropertyImpl', 'GetType', 'GetTypeArray', 'GetTypeCode', 'GetTypeCodeImpl', 'GetTypeFromCLSID', 'GetTypeFromHandle', 'GetTypeFromProgID', 'GetTypeHandle', 'HasElementType', 'HasElementTypeImpl', 'ImplementedInterfaces', 'InvokeMember', 'IsAbstract', 'IsAnsiClass', 'IsArray', 'IsArrayImpl', 'IsAssignableFrom', 'IsAutoClass', 'IsAutoLayout', 'IsByRef', 'IsByRefImpl', 'IsCOMObject', 'IsCOMObjectImpl', 'IsClass', 'IsConstructedGenericType', 'IsContextful', 'IsContextfulImpl', 'IsDefined', 'IsEnum', 'IsEnumDefined', 'IsEquivalentTo', 'IsExplicitLayout', 'IsGenericParameter', 'IsGenericType', 'IsGenericTypeDefinition', 'IsImport', 'IsInstanceOfType', 'IsInterface', 'IsLayoutSequential', 'IsMarshalByRef', 'IsMarshalByRefImpl', 'IsNested', 'IsNestedAssembly', 'IsNestedFamANDAssem', 'IsNestedFamORAssem', 'IsNestedFamily', 'IsNestedPrivate', 'IsNestedPublic', 'IsNotPublic', 'IsPointer', 'IsPointerImpl', 'IsPrimitive', 'IsPrimitiveImpl', 'IsPublic', 'IsSZArray', 'IsSealed', 'IsSecurityCritical', 'IsSecuritySafeCritical', 'IsSecurityTransparent', 'IsSerializable', 'IsSpecialName', 'IsSubclassOf', 'IsUnicodeClass', 'IsValueType', 'IsValueTypeImpl', 'IsVisible', 'MakeArrayType', 'MakeByRefType', 'MakeGenericType', 'MakePointerType', 'MemberType', 'MemberwiseClone', 'MetadataToken', 'Missing', 'Module', 'Name', 'Namespace', 'Overloads', 'ReferenceEquals', 'ReflectedType', 'ReflectionOnlyGetType', 'StructLayoutAttribute', 'ToString', 'TypeHandle', 'TypeInitializer', 'UnderlyingSystemType', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__overloads__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'get_Assembly', 'get_AssemblyQualifiedName', 'get_Attributes', 'get_BaseType', 'get_ContainsGenericParameters', 'get_CustomAttributes', 'get_DeclaredConstructors', 'get_DeclaredEvents', 'get_DeclaredFields', 'get_DeclaredMembers', 'get_DeclaredMethods', 'get_DeclaredNestedTypes', 'get_DeclaredProperties', 'get_DeclaringMethod', 'get_DeclaringType', 'get_DefaultBinder', 'get_FullName', 'get_GUID', 'get_GenericParameterAttributes', 'get_GenericParameterPosition', 'get_GenericTypeArguments', 'get_GenericTypeParameters', 'get_HasElementType', 'get_ImplementedInterfaces', 'get_IsAbstract', 'get_IsAnsiClass', 'get_IsArray', 'get_IsAutoClass', 'get_IsAutoLayout', 'get_IsByRef', 'get_IsCOMObject', 'get_IsClass', 'get_IsConstructedGenericType', 'get_IsContextful', 'get_IsEnum', 'get_IsExplicitLayout', 'get_IsGenericParameter', 'get_IsGenericType', 'get_IsGenericTypeDefinition', 'get_IsImport', 'get_IsInterface', 'get_IsLayoutSequential', 'get_IsMarshalByRef', 'get_IsNested', 'get_IsNestedAssembly', 'get_IsNestedFamANDAssem', 'get_IsNestedFamORAssem', 'get_IsNestedFamily', 'get_IsNestedPrivate', 'get_IsNestedPublic', 'get_IsNotPublic', 'get_IsPointer', 'get_IsPrimitive', 'get_IsPublic', 'get_IsSZArray', 'get_IsSealed', 'get_IsSecurityCritical', 'get_IsSecuritySafeCritical', 'get_IsSecurityTransparent', 'get_IsSerializable', 'get_IsSpecialName', 'get_IsUnicodeClass', 'get_IsValueType', 'get_IsVisible', 'get_MemberType', 'get_MetadataToken', 'get_Module', 'get_Name', 'get_Namespace', 'get_ReflectedType', 'get_StructLayoutAttribute', 'get_TypeHandle', 'get_TypeInitializer', 'get_UnderlyingSystemType', 'get_core_clr_security_level', 'op_Equality', 'op_Inequality']

# clr.AddReference("Zhu测试函数")

# a = AccessTools.Field(ClassType, "funcUpdatePrefix")
# print(a) # System.Func`2[UIBuildingGrid,System.Boolean] funcUpdatePrefix
Traverse.Create(ClassType).Field("funcUpdatePrefix").SetValue(System.Func[UIBuildingGrid, System.Boolean](Prefix))
Traverse.Create(ClassType).Field("funcUpdatePostfix").SetValue(System.Func[UIBuildingGrid, System.Boolean](Postfix))
# print(ClassType.funcUpdatePrefix) # 'RuntimeType' object has no attribute 'funcUpdatePrefix'
# print(ClassType.funcUpdatePostfix)


# ClassType.funcUpdatePrefix = System.Func[UIBuildingGrid, System.Boolean](Prefix)
# ClassType.funcUpdatePostfix = System.Func[UIBuildingGrid, System.Boolean](Postfix)

# print(ClassType.funcUpdatePrefix)
# print(ClassType.funcUpdatePostfix)
# method = AccessTools.Method(ClassType, "UpdatePrefix")
# print(method)
# print("Python: dll生成运行完成")
