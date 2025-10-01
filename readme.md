<div align="center" style="font-size: 42px; font-weight:bold;">Zhu-DspGame-Python3-Mod</div>

---

### 一、使用教程

1、得益于新多线程框架的戴森球计划游戏里的unity版本升级到了v2022.3.53，已经具备了运行了python3.13所需要的要求，不用再替换戴森球计划的自带的dll，只需把BepInEx文件夹复制到游戏安装目录下就能运行python。

2、安装python3脚本，把写好的脚本放到BepInEx\plugins\python3\mod文件夹里就行。注意您编写的脚本，需要包含Start()、Update()和OnGUI()这三个函数，至少是pass函数体。编写脚本可以参考BepInEx\plugins\python3\mod文件夹里的python脚本



### 二、已知问题

1、python3.13是单线程版本且是挂载在游戏主线程里的，而戴森球计划现在是多线程版本，这个导致了游戏开幕时，不能跳过序章。

播放序章时，戴森球计划有scan线程在后台生成星球，但由于python3.13的单线程特性和荒漠星添加石油mod，导致多线程生成星球的多线程特性失效变单线程，导致游戏加载过程变慢，此时跳过序章有概率卡死，等动画播放完了，降落在初始星。如果创建游戏时，星球数量少，此时大概能生成完，如果是128个星球以上，需要再等一段时间才能离开初始星球，防止出错。

2、可以用python编写System.Reflection.Emit的IL代码，再把python函数代理进去IL代码块运行即可，详细可以参考mod里dspharmony.py文件，这些操作都可以在python中进行，无需编写和编译C#代码。

3、经过测试，戴森球计划游戏中Assembly-CSharp.dll里面游戏用没有命名空间的类，pythonnet3.0.3自动绑定到python313引擎里了，只需要简单的LDB = clr.LDB 一行代码就可以直接调用，和import UnityEngine as ue这样一样方便调用。

```python
import clr
from System import Console
dll = clr.AddReference("Assembly-CSharp.dll")
LDB = clr.LDB
for i in LDB.items.dataArray:
    Console.WriteLine(i.Name)
```




### 三、感谢老天爷恩赐

以前能发现戴森球计划运行python3的正确途径，纯属意外，全靠老天爷恩赐。

我在ironpython2、ironpython3和pythonnet之间来回测试，一般都会删除掉BepInex插件文件夹里的测试dll（毕竟会报错）。那天我测试ironpython3，试了好几个处理，都是报错和平台不支持，我查找网页看到说，unity有2套运行时，为了stream上传要求的64位程序，厂商才会选用aot编译及发布。然后我突发奇想，报错既然是平台不支持，而unity的运行时是有2套，一套是aot，一套是jit。游戏的是aot运行时，会不会只要改下平台，ironpython3就能正常运行。结果出人意料，ironpython3没运行成功，反而在控制台里看到pythonnet运行了，查下下才发现是pythonnet3.0.3的dll忘删了。[笑脸]

事情就这么成了。全靠老天爷恩赐，感恩老天爷恩赐，[笑脸]
