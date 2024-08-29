import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetFactory, BuildTool_Click, BuildTool_Path, ConstructionSystem, CircleGizmo, Configs, Maths, GameGizmo
from dspharmony import HarmonyPatchDefaultPostfix
from UnityEngine import Vector3, Time, Quaternion, MeshRenderer, MotionVectorGenerationMode, Material, Color, Component, MeshFilter, Mesh
 
from UnityEngine.Rendering import ShadowCastingMode



def Start():
    SetTeleportGizmo()
    HarmonyPatchDefaultPostfix(BuildTool_Path, "UpdateRaycast", Postfix) 


def Update():
    pass


def OnGUI():
    pass




def Postfix(__instance):
    SetTeleportPosition(__instance.cursorTarget, __instance.planet)



teleportGizmo0 = None
teleportGizmo1 = None
def SetTeleportGizmo():
    global teleportGizmo0, teleportGizmo1
    pos = Vector3(1, 2, 3)
    teleportGizmo0 = CreatCircleGizmo(pos, 3, 1,    0.75)
    teleportGizmo1 = CreatCircleGizmo(pos, 4, 1.35, 1)


def CreatCircleGizmo(position, texid, radius, percent):
    gameObject = 复制对象(Configs.builtin.circleGizmoPrefab.gameObject, GameGizmo.gizmoGroup)
    # gameObject = 复制对象网格(Configs.builtin.circleGizmoPrefab.gameObject)

    gameObject.SetActive(True)
    gameObject.transform.forward = position.normalized
    gameObject.transform.position = position
    gameObject.transform.localScale = Vector3(radius, radius, radius)

    circleRenderer = gameObject.GetComponent[MeshRenderer]()
    circleRenderer.sharedMaterial = CreatCircleMaterial(texid, percent)
    circleRenderer.shadowCastingMode = ShadowCastingMode.Off
    circleRenderer.receiveShadows = False
    circleRenderer.motionVectorGenerationMode = MotionVectorGenerationMode.ForceNoMotion
    return gameObject




def 复制对象(fromObject, parentTransform):
    gameObject = UnityEngine.Object.Instantiate[UnityEngine.GameObject](fromObject, parentTransform)
    gameObject = 删除对象脚本(gameObject)
    return gameObject


def 复制对象网格(fromObject, parentTransform=None):
    gameObject = UnityEngine.GameObject() # 新建游戏对象时，自动添加 gameObject.AddComponent[Transform]()，其他 Component 需手动添加
    gameFilter = gameObject.AddComponent[MeshFilter]()
    gameRenderer = gameObject.AddComponent[MeshRenderer]()
    # for component in gameObject.GetComponents[Component](): print(type(component))

    fromFilter = fromObject.GetComponent[MeshFilter]()
    if fromFilter != None: gameFilter.mesh = UnityEngine.Object.Instantiate[UnityEngine.Mesh](fromFilter.mesh)

    gameObject.transform.SetParent(fromObject.transform.parent) # 未设置是直接挂在场景根节点
    if parentTransform != None: gameObject.transform.SetParent(parentTransform) # 统一挂在了 GameGizmo.gizmoGroup Transform 下了
    # 经过测试，gameObject挂在根场景下，不会影响圆圈在戴森球计划游戏里的各个星球的显示

    return gameObject


def 删除对象脚本(gameObject):
    脚本 = gameObject.GetComponent[CircleGizmo]() # 获取 MonoBehaviour Component
    if 脚本 != None: UnityEngine.GameObject.Destroy(脚本) # for component in gameObject.GetComponents[Component](): print(type(component))
    return gameObject



def CreatCircleMaterial(texid=3, percent=1):
    circleMaterial = UnityEngine.Object.Instantiate[Material](Configs.builtin.circleGizmoMat)
    circleMaterial.mainTexture = Configs.builtin.circleTextures[texid]
    circleMaterial.SetColor("_TintColor", Configs.builtin.gizmoColors[4]) # color = Configs.builtin.gizmoColors[4]
    circleMaterial.SetFloat("_Multiplier", 2.5)
    circleMaterial.SetFloat("_AlphaMultiplier", 0.7)
    circleMaterial.SetFloat("_Percent", percent)
    return circleMaterial


def SetTeleportPosition(position, planet): # 百分比
    if position == Vector3.zero: return # [Warning: Unity Log] bad query # [Info   : Unity Log] Look rotation viewing vector is zero

    # height = planet.data.QueryHeight(position) # 原始地面高度 Query：查询
    height = planet.data.QueryModifiedHeight(position) # 修改后的地面高度
    position = position.normalized * height

    teleportGizmo0.transform.forward = position.normalized
    teleportGizmo0.transform.position = position

    teleportGizmo1.transform.forward = position.normalized
    teleportGizmo1.transform.position = position


    圆圈动画(position)


rotateSpeed0 = 50
rotateSpeed1 = 60

time = 0
def 圆圈动画(position):
    global time
    time += Time.deltaTime
    if time > 60: time = 0
    teleportGizmo0.transform.localRotation = Maths.SphericalRotation(position, time * rotateSpeed0) * Quaternion.Euler(90, 0.0, 0.0)
    teleportGizmo1.transform.localRotation = Maths.SphericalRotation(position, time * rotateSpeed1) * Quaternion.Euler(90, 0.0, 0.0)

    # teleportGizmo0.transform.localRotation = Quaternion.Euler(0.0, time * rotateSpeed0, 0.0) * Quaternion.Euler(90, 0.0, 0.0)
    # teleportGizmo1.transform.localRotation = Quaternion.Euler(0.0, time * rotateSpeed1, 0.0) * Quaternion.Euler(90, 0.0f, 0.0)