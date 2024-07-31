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


namespace Python3Mod
{
    [BepInPlugin(GUID, NAME, VERSION)]
    [BepInProcess(GAME_PROCESS)]
    public class Plugin : BaseUnityPlugin
    {
        public const string GUID = "cn.zhufile.dsp.zhu_python3_mod";
        public const string NAME = "Python3Mod";
        public const string VERSION = "1.0.7";
        private const string GAME_PROCESS = "DSPGAME.exe";

        public static bool 存在Python = false;
        public static float time = 0;



        public void Start() 
        {

            Runtime.PythonDLL = ".\\BepInEx\\plugins\\Python3Mod\\Python311Embed\\python311.dll";
            PythonEngine.Initialize();
            using (Py.GIL())
            {
                //var scope = Py.CreateScope();
                //scope.Set("items", LDB.items.dataArray);
                
                //dynamic clr = Py.Import("clr");
                //var lib = clr.AddReference("Assembly-CSharp.dll");
                //Console.WriteLine(lib);

                dynamic sys = Py.Import("sys");
                sys.path.append(".\\BepInEx\\plugins\\Python3Mod\\libs"); //sys.path.append(Path.GetFullPath(".\\BepInEx\\plugins\\Python3Mod\\libs"));
                sys.path.append(".\\BepInEx\\plugins\\Python3Mod\\mod");
                sys.path.append(".\\BepInEx\\plugins\\Python3Mod\\modmanage");
                //foreach (var modpath in sys.path)
                //    Console.WriteLine(modpath);
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


                //if (UIRoot.instance == null || GameMain.instance == null)
                //    return;


                //time += Time.deltaTime;
                //if (time > 10)
                //{
                //    using (Py.GIL())
                //    {
                //        dynamic manage = Py.Import("manage");
                //        //var type = LDB;
                //        //// var type = typeof(LDB);
                //        //manage.LDB = type;
                //        //Console.WriteLine(type);
                //        manage.items = LDB.items.dataArray;
                //        manage.打印();
                //    }
                //    time = 0;
                //}


                //Type myType = typeof(MyClass);

                //// 使用Activator创建实例
                //object myInstance = Activator.CreateInstance(myType);

                //// 如果需要强制转换到特定类型
                //MyClass myTypedInstance = (MyClass)myInstance;

                //Console.WriteLine("实例创建成功！");


            }
        public void OnGUI()
        {
            //if (UIRoot.instance == null || GameMain.instance == null)
            //    return;
            using (Py.GIL())
            {
                dynamic manage = Py.Import("manage");
                //manage.items = LDB.items.dataArray;
                manage.OnGUI();
            }
        }

    }


}




