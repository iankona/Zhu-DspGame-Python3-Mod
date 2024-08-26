import System

from dsptype import PlanetFactory, BuildTool_Click, BuildTool_Path, ConstructionSystem, CircleGizmo, Configs, Maths
from dspharmony import HarmonyPatchDefaultPrefixWithReturn, HarmonyPatchDefaultPrefix, HarmonyPatchDefaultPostfix
from UnityEngine import Vector3, Time, Quaternion

def Start():
    SetTeleportGizmo()
    HarmonyPatchDefaultPostfix(BuildTool_Path, "UpdateRaycast", Postfix) 


def Update():
    pass


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
    teleportGizmo0 = CircleGizmo.Create(3, pos, gizmoRadius)
    teleportGizmo0.multiplier = 4.5
    teleportGizmo0.alphaMultiplier = 1
    teleportGizmo0.fadeInScale = 1.3
    teleportGizmo0.fadeInTime = 0.13
    teleportGizmo0.fadeInFalloff = 0.5
    teleportGizmo0.color = Configs.builtin.gizmoColors[4]
    teleportGizmo0.rotateSpeed = 45
    teleportGizmo0.percent = 0.75 # 默认1.0
    teleportGizmo0.Open()
    teleportGizmo0.RefreshRotation()
    
    teleportGizmo1 = CircleGizmo.Create(4, pos, gizmoRadius * 1.25)
    teleportGizmo1.color = Configs.builtin.gizmoColors[4]
    teleportGizmo1.multiplier = 2
    teleportGizmo1.alphaMultiplier = 0.7
    teleportGizmo1.fadeInScale = 1.3
    teleportGizmo1.fadeInTime = 0.13
    teleportGizmo1.fadeInFalloff = 0.5
    teleportGizmo1.rotateSpeed = 60
    teleportGizmo1.Open()
    teleportGizmo1.RefreshRotation()


def SetTeleportPercent(percent): # 百分比
    if teleportGizmo0 == None or teleportGizmo0.active == False:
        return
    teleportGizmo0.percent = percent

def SetTeleportPosition(pos, planet): # 百分比
    if pos == Vector3.zero: return # [Warning: Unity Log] bad query # [Info   : Unity Log] Look rotation viewing vector is zero
    if teleportGizmo0 == None: SetTeleportGizmo(pos)
        
    height = planet.data.QueryHeight(pos)
    pos = pos.normalized * height

    teleportGizmo0.gameObject.SetActive(True)
    teleportGizmo0.transform.forward = pos.normalized # 球行的
    teleportGizmo0.transform.position = pos
    teleportGizmo0.position = pos


    teleportGizmo1.gameObject.SetActive(True)
    teleportGizmo1.transform.forward = pos.normalized
    teleportGizmo1.transform.position = pos
    teleportGizmo1.position = pos


