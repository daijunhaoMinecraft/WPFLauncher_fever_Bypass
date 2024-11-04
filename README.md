# WPFLauncher_fever_Bypass
网易我的世界发烧平台绕过<br />
**请注意:此软件里面含有修改hosts操作,所以使用此软件需要以管理员身份运行!**<br />
**此方法目前暂时不进行维护(主要原因是能稳定很久),这边建议使用功能更强大的[网易我的世界Hook注入](https://github.com/daijunhaoMinecraft/WPFLauncher_Hook)(需安装[.NET6.0的sdk](https://dotnet.microsoft.com/zh-cn/download/dotnet/thank-you/sdk-6.0.425-windows-x86-installer)),该项目会进行长期维护**<br />
# 事情起因
由于我实在受不了发烧平台<br />
于是就去B站搜发烧平台绕过方法,结果<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/84060f7e-d8ae-443c-8811-ec1251475172)<br />
既然找不到合适的绕过,那就自己写一个绕过程序吧<br />
# 绕过原理
这是网易的更新,然后访问这个网址:<https://x19.update.netease.com/pl/x19_java_patchlist><br />
这里面就是启动器所有版本(包括大小,替换包直连地址,MD5)<br />
我们将里面的内容修改成<br />
"xxx":{"size": xxx, "url": "xxx", "md5": "xxx"},<br />
就可以实现绕更新<br />
但关键是我门要如何修改呢?<br />
在127.0.0.1建立一个80端口的网站<br />
里面的内容替换成:"xxx":{"size": xxx, "url": "xxx", "md5": "xxx"},<br />
我们通过hosts修改成127.0.0.1 x19.update.netease.com<br />
这样就可以实现绕更新了
# 使用方法
去到Release,下载最新版WPFLauncher_Loader.7z,全部解压<br />
之后保存到一个路径下,因为你每次启动游戏都要打开WPFLauncher_Loader.exe这个文件,同时你也要确保这个exe所在的文件夹下有server.crt和server.key这俩个文件<br />
然后打开WPFLauncher_Loader.exe,刚开始如果检测到发烧平台,会自动卸载发烧平台并卸载网易我的世界启动器(这个网易我的世界启动器是与发烧平台配套的,如果没有,则会提示去发烧平台那边启动游戏)然后会自动下载网易我的世界启动器并安装(默认C盘,我也不知道如何更改路径,如果要更改路径请到[网易我的世界官网](https://mc.163.com/)上下载32位包体并安装),后面每次启动就需要打开WPFLauncher_Loader.exe
# 效果展示
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/7a80e3f6-5eae-4438-bbfa-7d39f0bbab58)<br />
游戏是可以正常登录的
