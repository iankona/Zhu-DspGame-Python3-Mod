using UnityEngine;

using BepInEx;
using HarmonyLib;

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Reflection;
using System.Text;

using Python.Runtime;
using System.IO;


namespace PythonNetMod
{
    [BepInPlugin(GUID, NAME, VERSION)]
    [BepInProcess(GAME_PROCESS)]
    public class Plugin : BaseUnityPlugin
    {
        public const string GUID = "cn.zhufile.dsp.zhu_python3_mod";
        public const string NAME = "Python3Mod";
        public const string VERSION = "0.8.1";
        private const string GAME_PROCESS = "DSPGAME.exe";

        public void Start() 
        {
            Runtime.PythonDLL = ".\\BepInEx\\plugins\\python3\\python3embed\\python313.dll";
            PythonEngine.Initialize();
            using (Py.GIL())
            {
                dynamic sys = Py.Import("sys");
                sys.path.append(".\\BepInEx\\plugins\\python3\\python3libs"); //sys.path.append(Path.GetFullPath(".\\BepInEx\\plugins\\Python3Mod\\libs"));
                sys.path.append(".\\BepInEx\\plugins\\python3\\mod");
                sys.path.append(".\\BepInEx\\plugins\\python3\\modmanage");
            }
            using (Py.GIL())
            {
                dynamic manage = Py.Import("manage");
                manage.Start();
            }
        }


        public void Update()
        {
            using (Py.GIL())
            {
                dynamic manage = Py.Import("manage");
                manage.Update();
            }
        }


        public void OnGUI()
        {
            using (Py.GIL())
            {
                dynamic manage = Py.Import("manage");
                manage.OnGUI();
            }
        }

    }


}




