# WPFLauncher_fever_Bypass
网易我的世界发烧平台绕过<br />
# 事情起因
由于我实在受不了发烧平台<br />
于是就去B站搜发烧平台绕过方法,结果<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/84060f7e-d8ae-443c-8811-ec1251475172)<br />
既然找不到合适的绕过,那就自己写一个绕过程序吧<br />
# 绕过原理
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/a007b889-def1-433b-82b2-231f2ddc13ab)<br />
通过python抓包,我们可以发现最后一个没有发烧平台的版本是1.13.2.35313,下一个版本1.13.3.35796的更新日志是有这么写到(1.13.3.35796)<br />
"为了带来更好的游戏体验，《我的世界》端游官网包将于3月19日——3月26日期间逐步迁移至发烧游戏平台上进行启动。届时游戏将会自动完成平台更新，冒险家的正常游玩体验不会受到任何影响。"<br />
更好的游戏体验(确信)<br />
因此我下载了1.13.2.35313(最后一个没有发烧平台的版本)替换包,里面的内容是这样:<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/a9852b9e-494d-4a35-b591-e5ab66c8ff81)<br />
而1.13.3.35796的替换包,里面的内容是这样:<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/c4c01792-02fe-4f6a-922a-7301666c0e6b)<br />
因此我就可以断定1.13.2.35313之前的版本(包括1.13.2.35313)是没有发烧平台的提示,反倒是1.13.3.35796之后的版本(包括1.13.3.35796)就开始会出现提示了<br />
然后把里面的文件替换后会出现以下情况:<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/55c8faff-1d6d-4399-8b5c-97f92dc22f00)<br />
这是网易的更新,然后访问这个网址:<https://x19.update.netease.com/pl/x19_java_patchlist><br />
这里面就是启动器所有版本(包括大小,替换包直连地址,MD5)<br />
其中我们需要关注这一行<br />
"1.13.2.35313":{"size": 82762233, "url": "https://x19.gph.netease.com/patch1.13.2.35313.X19.Release.7z", "md5": "452234882051b35454941b40991cd93a"},<br />
我们通过hosts修改成127.0.0.1 x19.update.netease.com<br />
然后将127.0.0.1里面的内容替换成:"1.13.2.35313":{"size": 82762233, "url": "https://x19.gph.netease.com/patch1.13.2.35313.X19.Release.7z", "md5": "452234882051b35454941b40991cd93a"},<br />
这样就可以实现绕更新了
# 使用方法
首先我们要先卸载发烧平台和网易我的世界启动器<br />
然后去到[我的世界官网](https://mc.163.com)<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/de904b6c-5b9d-4273-98ce-142ed77a92d9)<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/c1b82f4b-3f1d-4e79-ba10-7ddb1e5d533e)<br />
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/6c2738f3-c18c-4cc3-b2de-f88ea4d5c03e)<br />
之后去到Release,下载最新版WPFLauncher_Loader.7z,全部解压<br />
之后保存到一个路径下,因为你每次启动游戏都要打开WPFLauncher_Loader.exe这个文件,同时你也要确保这个exe所在的文件夹下有server.crt和server.key这俩个文件<br />
然后打开WPFLauncher_Loader.exe,刚开始会让你下载替换包,后面每次启动就不会了(除非启动器重装)
# 效果展示
![image](https://github.com/daijunhaoMinecraft/WPFLauncher_fever_Bypass/assets/121751847/7a80e3f6-5eae-4438-bbfa-7d39f0bbab58)<br />
游戏是可以正常登录的
