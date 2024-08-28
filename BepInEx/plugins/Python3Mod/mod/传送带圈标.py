import System
import UnityEngine

from HarmonyLib import AccessTools, Traverse

from dsptype import PlanetFactory, BuildTool_Click, BuildTool_Path, ConstructionSystem, CircleGizmo, Configs, Maths, GameGizmo
from dspharmony import HarmonyPatchDefaultPrefixWithReturn, HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix
from UnityEngine import Vector3, Time, Quaternion, Material


def Start():
    HarmonyPatchDefaultPostfix(BuildTool_Path, "UpdateRaycast", Postfix) 

time = 0
def Update():
    global time
    time += Time.deltaTime
    if time > 60:
        time = 0
        Traverse.Create(teleportGizmo0).Field("time").SetValue(System.Single(0.25))
        # Traverse.Create(teleportGizmo0).Field("destroyTime").SetValue(System.Single(0.0))
        Traverse.Create(teleportGizmo1).Field("time").SetValue(System.Single(0.25))
        # Traverse.Create(teleportGizmo1).Field("destroyTime").SetValue(System.Single(0.0))


def OnGUI():
    pass




def Postfix(__instance):
    SetTeleportPosition(__instance.cursorTarget, __instance.planet)



gizmoRadius = 0.35
teleportGizmo0 = None
teleportGizmo1 = None
def SetTeleportGizmo():
    global teleportGizmo0, teleportGizmo1
    pos = Vector3(1,2,3)
    pos = pos.normalized * (pos.magnitude + 0.1)
    # teleportGizmo0 = CircleGizmo.Create(3, pos, gizmoRadius)

    teleportGizmo0 = UnityEngine.Object.Instantiate[CircleGizmo](Configs.builtin.circleGizmoPrefab, GameGizmo.gizmoGroup)
    # teleportGizmo0 = UnityEngine.Object.Instantiate[UnityEngine.GameObject](Configs.builtin.circleGizmoPrefab.gameObject)
    teleportGizmo0.Reset() # gameObject not Reset
    teleportGizmo0.transform.position = pos
    teleportGizmo0.textureIndex = 3
    teleportGizmo0.position = pos
    teleportGizmo0.radius = gizmoRadius

    teleportGizmo0.color = Configs.builtin.gizmoColors[4]
    teleportGizmo0.multiplier = 4.5
    teleportGizmo0.alphaMultiplier = 1
    teleportGizmo0.fadeInScale = 1.3
    teleportGizmo0.fadeInTime = 0.13
    teleportGizmo0.fadeInFalloff = 0.5
    teleportGizmo0.rotateSpeed = 45
    teleportGizmo0.percent = 0.75 # 默认1.0


    teleportGizmo1 = UnityEngine.Object.Instantiate[CircleGizmo](Configs.builtin.circleGizmoPrefab, GameGizmo.gizmoGroup)
    # teleportGizmo1 = UnityEngine.Object.Instantiate[UnityEngine.GameObject](Configs.builtin.circleGizmoPrefab.gameObject)
    teleportGizmo1.Reset()
    teleportGizmo1.transform.position = pos
    teleportGizmo1.textureIndex = 4
    teleportGizmo1.position = pos
    teleportGizmo1.radius = gizmoRadius * 1.35

    teleportGizmo1.color = Configs.builtin.gizmoColors[4]
    teleportGizmo1.multiplier = 2
    teleportGizmo1.alphaMultiplier = 0.7
    teleportGizmo1.fadeInScale = 1.3
    teleportGizmo1.fadeInTime = 0.13
    teleportGizmo1.fadeInFalloff = 0.5
    teleportGizmo1.rotateSpeed = 60
    # teleportGizmo0.percent = 1.0 # 默认1.0



def SetTeleportPercent(percent): # 百分比
    if teleportGizmo0 == None or teleportGizmo0.active == False: return
    teleportGizmo0.percent = percent


def SetTeleportPosition(pos, planet): 
    if pos == Vector3.zero: return # [Warning: Unity Log] bad query # [Info   : Unity Log] Look rotation viewing vector is zero
    if teleportGizmo0 == None or teleportGizmo1 == None: SetTeleportGizmo()
        
    # height = planet.data.QueryHeight(pos) # 原始地面高度 Query：查询
    height = planet.data.QueryModifiedHeight(pos) # 修改后的地面高度
    pos = pos.normalized * height

    teleportGizmo0.Open()

    teleportGizmo0.transform.forward = pos.normalized # 球行的
    teleportGizmo0.transform.position = pos
    teleportGizmo0.position = pos

    teleportGizmo1.Open()

    teleportGizmo1.transform.forward = pos.normalized
    teleportGizmo1.transform.position = pos
    teleportGizmo1.position = pos


