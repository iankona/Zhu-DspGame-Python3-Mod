<div align="center" style="font-size: 42px; font-weight:bold;">Zhu-DspGame-Python3-Mod</div>

---

### 一、使用教程

1、把戴森球计划（Dyson Sphere Program Game）安装目录里的DSPGAME_Data\Managed文件夹复制一份，用于备份。

2、把这里的Managed里的所有dll复制到戴森球计划安装目录里的DSPGAME_Data\Managed文件夹，覆盖掉原来的dll，使游戏由原来的Unity2018.4.12f1_unityaot运行时变成Unity2018.4.12f1_unityjit运行时。经测试原来的aot运行时mod依然能正常使用，但如果出现问题，请把备份的原游戏的Managed复制回去。

3、安装戴森球计划python3Mod插件。把这里的BepInEx文件复制到游戏安装目录下就行。

4、安装python3Mod，把python3Mod库或脚本放到安装好后的插件文件里面的mod文件夹里。

5、启用python3Mod，编辑安装好后的插件文件里面的modmanage文件夹里的manage.py文件，import您编写的脚本，然后在manage.py文件里Start()、Update()和OnGUI()三个函数里添加您的对应的运行函数即可。



### 二、已知问题

1、UnityEngine的GUI的Window函数有问题，出错原因是python函数无法转换成C#函数。请使用GUI.BeginClip()和GUI.EndClip()替换GUI.Window()函数的功能

~~2、pythonnet3.0.3导入Assembly-CSharp.dll有问题，出错原因是戴森球计划游戏的功能类都是没有命名空间的，dll导入后，这些没有命名空间的类会被跳过，没有进行python3绑定，所以没法像import UnityEngine as ue这样方便调用，您需要使用反射等方式，单独调用这些类型。~~

~~（笔者修改代码，使得这些没有空间的类加入处理队列，但还是遇到模块里没有这些类的python报错，说明这个处理在pythonnet中可能更加底层，不是笔者简单改改能起作用的）。~~

~~使用Assembly-CSharp.dll里这些没有命名空间的类型，参考代码如下，代码仅演示属性调用，函数调用是另外的代码。~~

~~这些调用很繁琐，没有像有命名空间的类型那样直接import调用方便。~~

~~期待pythonnet能早日支持这些没有命名空间的类型自动进行python3绑定，不要在这么繁琐的调用，这一点也不python啊，把他们自动处理进GlobalAssembly空间也行啊~~

```python
import clr
from System import Console
dll = clr.AddReference("Assembly-CSharp.dll")
LDB = dll.GetType("LDB")
items = LDB.GetProperty("items").GetValue(None)
for i in items.dataArray:
    Console.WriteLine(i.Name)
```

2、经过测试，发现戴森球计划游戏中Assembly-CSharp.dll里面这些没有命名空间的类，pythonnet3.0.3也自动绑定到python311了，只需要简单的LDB = clr.LDB 一行代码就可以直接调用，和import UnityEngine as ue这样方便调用，这样编写脚本的环境基础就齐活了。[掩嘴笑]

```python
import clr
from System import Console
dll = clr.AddReference("Assembly-CSharp.dll")
LDB = clr.LDB
for i in LDB.items.dataArray:
    Console.WriteLine(i.Name)
```




### 三、下面其他这些，不重要，可以跳过

1、使用unityjit的dll编译pyhtonnet。把pyhtonnet的github网站上的源码下载下来，正常编译一遍，然后在依赖里的netstandard2.0.3条目上鼠标右键，打开文件夹位置，进入到存dll的文件夹，把里面的dll都删除，再把Unity2018.4.12f1JIT里面的dll复制进去，再重新编译一遍pyhtonnet。编译结果文件夹里的netstandard2.0.3里的Python.Runtime.dll是所需要的。

（这个可能不是重点，但用unityJIt重新编译下，应该更不会出错。JIT编译的Python.Runtime.dll能用了之后，我也没有再去测试其他编译出来的dll）

（游戏运行时由unityaot改unityJIT才是运行python3的重点，而且我测试，游戏本体和mod都能正常运行（这可能和我测试的mod较少有关[掩嘴笑]））

2、初始化python3环境，经过测试好像只能在Start()函数里进行（Awake()没测试过，不清楚），在Update()里初始化，会出错，可能和主线程相关限制有关，这个不清楚。

3、下载Unity2018.4.12f1的SDK。

①安装Unity Hub，安装好后，打开Unity Hub，

②打开浏览器，把unityhub://2018.4.12f1/59ddc4c59b4f 复制到浏览器地址栏，回车，在弹出的小栏目，选择打开Unity Hub，

③在跳出的界面，选择Window Build Support (IL2CPP)，选择简体语言包，选择Documentation就行（其他选项点掉，不用选）

④在跳出的界面，选择右下方的继续按钮，就开始自动下载和安装了，安装完了就可以关闭Unity Hub，然后到安装目录里面复制dll了。

4、ironpython2，用unityJIT编译成功，但使用会出现平台不支持报错，原因不明。

5、ironpython3，编译就不通过，更不用谈使用了。ironpython3编译不通过的原因是ironpython3大量使用了System.Memory4.5.5中的功能，而我看到的，直到unity2020，unity使用的是System.Memory4.0.0，缺少了很大一部分功能，用其他繁琐代码替换修改，都没法替换的那种。

```
<ItemGroup>
    <PackageReference Include="System.Memory" Version="4.5.5" />
</ItemGroup>
```

6、编译的依赖库问题，为了减少麻烦，我编译目标是选netstandard2.0，先正常编译一次，等里面出现了系统nuget自动下载配置好的netstandard.library文件夹，然后我在文件夹里面放置不同的每套dll，这样就能重新编译出对应的dll。

7、编译环境。

Community Visual Studia 2022

Unity2018.4.12f1

pythonnet3.0.3

python-3.11.9-embed-amd64.zip

[Message:   BepInEx] BepInEx 5.4.23.2 - DSPGAME (2024/7/25 19:52:32)

[Info   :   BepInEx] Running under Unity v2018.4.12.5889476

[Info   :   BepInEx] CLR runtime version: 4.0.30319.42000

[Info   :   BepInEx] Supports SRE: True

[Info   :   BepInEx] System platform: Bits64, Windows




### 四、感谢老天爷恩赐

这次能发现戴森球计划运行python3Mod的正确途径，纯属意外，全靠老天爷恩赐。

我在ironpython2、ironpython3和pythonnet之间来回测试，一般都会删除掉BepInex插件文件夹里的测试dll（毕竟会报错）。那天我测试ironpython3，试了好几个处理，都是报错和平台不支持，我查找网页看到说，unity有2套运行时，为了stream上传要求的64位程序，厂商才会选用aot编译及发布。然后我突发奇想，报错既然是平台不支持，而unity的运行时是有2套，一套是aot，一套是jit。游戏的是aot运行时，会不会只要改下平台，ironpython3就能正常运行。所以我覆盖了一下游戏dll，但结果出来的是正确的python3结果，把我意外了，我查了下，原来是我dll忘删了。

事情就这么成了。全靠老天爷恩赐，感恩老天爷恩赐，[笑脸]
