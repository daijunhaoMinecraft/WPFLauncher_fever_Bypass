# -*- coding:utf-8 -*-
#修复网络信号不佳问题
import sys
print("检查hosts文件...")
# 打开C:\Windows\System32\drivers\etc\hosts文件，读取内容
with open(r"C:\Windows\System32\drivers\etc\hosts", "r", encoding="utf-8") as f:
    if "\n127.0.0.1 x19.update.netease.com" in f.read():
        print("发现hosts文件中存在127.0.0.1 x19.update.netease.com,正在删除...")
        get_hosts = f.read().replace("\n127.0.0.1 x19.update.netease.com", "")
        # 打开C:\Windows\System32\drivers\etc\hosts文件，写入内容
        with open(r"C:\Windows\System32\drivers\etc\hosts", "w", encoding="utf-8") as f:
            f.write(get_hosts)
        print("修改完毕,按Enter键退出")
        input()
        sys.exit()
    else:
        print("hosts文件中不存在127.0.0.1 x19.update.netease.com")
        print("按Enter键退出")
        input()
        sys.exit()