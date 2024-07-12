import http.server
import json
import socketserver
import ssl
import sys
import re
import threading
import winreg
import os
import win32api
import time
import requests
from urllib.parse import urlparse
from tqdm.rich import tqdm
import psutil
import subprocess
import warnings
from py7zr import SevenZipFile
warnings.simplefilter("ignore")
import atexit
@atexit.register
def atexit_fun():
    # 打开C:\Windows\System32\drivers\etc\hosts文件，读取内容
    with open(r"C:\Windows\System32\drivers\etc\hosts", "r", encoding="utf-8") as f:
        get_hosts = f.read().replace("\n127.0.0.1 x19.update.netease.com", "")
    # 打开C:\Windows\System32\drivers\etc\hosts文件，写入内容
    with open(r"C:\Windows\System32\drivers\etc\hosts", "w", encoding="utf-8") as f:
        f.write(get_hosts)

# 定义一个函数，用于根据端口号查找进程
def find_process_by_port(port):
    # 遍历所有进程
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            # 获取进程的连接信息
            connections = proc.connections()
            # 遍历连接信息
            for conn in connections:
                # 如果连接信息的端口号与给定的端口号相等
                if conn.laddr.port == port:
                    # 返回该进程
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # 如果出现异常，则继续遍历下一个进程
            pass
    # 如果找不到进程，则返回None
    return None


def kill_process(proc):
    try:
        proc.terminate()
        print(f"终止进程pid:{proc.pid}")
    except psutil.AccessDenied:
        print(f"使用pid终止进程时访问被拒绝:{proc.pid}")
    except psutil.NoSuchProcess:
        print(f"此pid进程不存在:{proc.pid}")

#重连次数
requests.adapters.DEFAULT_RETRIES = 5
#获取当前执行exe的路径
pathx_pyinstaller = os.path.dirname(os.path.realpath(sys.argv[0]))
#获取当前path路径
pathx = os.path.dirname(os.path.realpath(sys.argv[0]))
#忽略证书警告
requests.packages.urllib3.disable_warnings()
#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}

def download_nofilename(url, save):
    '''
    下载文件，但不指定文件名
    :param url: 下载文件的URL
    :param save: 保存文件的文件夹路径
    :return: None
    '''
    # 设置请求头
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
    # 重连次数
    reset_connect = 1
    while True:
        try:
            # 下载文件
            download_file = requests.get(url,headers=headers,verify=False,stream=True,timeout=60)
            break
        except Exception:
            # 下载失败，重新下载
            print(f"下载失败,正在重新下载,重连次数:{str(reset_connect)}")
            reset_connect += 1
    # 获取文件大小
    download_file_size = int(download_file.headers['Content-Length'])/1024
    # 获取文件名
    file_name = os.path.basename(urlparse(url).path)
    # 保存文件
    with open(file=f"{save}\\{file_name}", mode="wb") as f:
        # 进度条
        for data in tqdm(iterable=download_file.iter_content(1024),total=download_file_size,unit='KB',desc=f"正在下载文件:{file_name}"):
            f.write(data)
# 定义一个函数，用于获取指定url的内容
def get_def(url):
    # 打开系统hosts文件，读取内容
    with open(r"C:\Windows\System32\drivers\etc\hosts", "r", encoding="utf-8") as f:
        get_hosts = f.read().replace("\n127.0.0.1 x19.update.netease.com", "")
        f.close()
    # 打开系统hosts文件，写入内容
    with open(r"C:\Windows\System32\drivers\etc\hosts", "w", encoding="utf-8") as f:
        f.write(get_hosts)
        f.close()
    # 获取指定url的内容
    get_content = requests.get(url,headers={"Host": "x19.update.netease.com"},verify=False).text
    # 打开系统hosts文件，添加一条规则
    with open(r"C:\Windows\System32\drivers\etc\hosts", "a+", encoding="utf-8") as f:
        f.write("\n127.0.0.1 x19.update.netease.com")
    # 返回获取到的内容
    return get_content

#获取当前执行exe的路径
pathx_pyinstaller = os.path.dirname(os.path.realpath(sys.argv[0]))
def get_file_version(file_path):
    '''获取文件版本号'''
    # 使用try语句，捕获异常
    try:
        # 获取文件版本信息
        info = win32api.GetFileVersionInfo(file_path, '\\')
        # 返回版本号字符串
        return '{0}.{1}.{2}.{3}'.format(
            info['FileVersionMS'] >> 16,
            info['FileVersionMS'] & 0xFFFF,
            info['FileVersionLS'] >> 16,
            info['FileVersionLS'] & 0xFFFF
        )
    except Exception as e:
        # 打印异常信息
        print("Error:", e)
        # 返回None
        return None
try:
    get_installer = str(winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, 'FeverGames'), "URL Protocol")[0]).replace('"', '')
    print("检测到发烧平台,正在静默卸载...")
    process = subprocess.Popen(f'"{get_installer.replace(os.path.basename(get_installer), "")}\\unins000.exe" /SILENT', stdout=subprocess.PIPE,universal_newlines=True, encoding="utf-8")
    process.wait()
    print("卸载完成,正在卸载网易我的世界启动器")
    print("检测启动器版本...")
    try:
        key_netease = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\MCLauncher')
        netease_path = winreg.QueryValueEx(key_netease, "InstallLocation")[0]
        netease_version = get_file_version(f"{netease_path}\\WPFLauncher.exe")
        print(f"当前网易我的世界版本:{str(netease_version)},开始卸载...")
        process = subprocess.Popen(f'"{netease_path}\\uninstall.exe" /SILENT', stdout=subprocess.PIPE,universal_newlines=True, encoding="utf-8")
        process.wait()
        print("卸载完成")
    except Exception as e:
        pass
except Exception as e:
    print("未发现发烧平台,检测我的世界启动器版本...")

try:
    key_netease = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\MCLauncher')
    netease_path = winreg.QueryValueEx(key_netease, "InstallLocation")[0]
    netease_version = get_file_version(f"{netease_path}\\WPFLauncher.exe")
    print(f"当前网易我的世界版本:{str(netease_version)}")
except Exception as e:
    print("未发现启动器,正在下载启动器安装包")
    match = re.search(r'var pc_link = "(.*?)";',requests.get("https://adl.netease.com/d/g/mc/c/pc?type=pc", headers=headers, verify=False).text,re.DOTALL)
    if match:
        get_wpflauncher_installer = match.group(1)
        print(f"获取到我的世界启动器安装包下载地址:{get_wpflauncher_installer},正在下载")
        download_nofilename(get_wpflauncher_installer,pathx_pyinstaller)
        if os.path.exists(f"{pathx_pyinstaller}\\{os.path.basename(urlparse(get_wpflauncher_installer).path)}"):
            print("下载完成,正在执行静默安装")
            process = subprocess.Popen(f'"{pathx_pyinstaller}\\{os.path.basename(urlparse(get_wpflauncher_installer).path)}" /silent /verisilent /norestart',stdout=subprocess.PIPE, universal_newlines=True, encoding="utf-8")
            process.wait()
            print("安装完成")
print("正在检测端口占用情况")
port = 443
process = find_process_by_port(port)
if process:
    kill_process(process)
else:
    print(f"恭喜,未发现443端口被占用的情况")
print("端口占用检测完成,正在启动游戏...")
print("检查更新")
data = requests.get("https://x19.update.netease.com/pl/x19_java_patchlist",headers=headers,verify=False).text
# 去掉文本开头和结尾的三重引号
data = data.strip()
# 去掉每行末尾的逗号
data = data.rstrip(',')
# 将所有的单引号替换为双引号
data = data.replace("'", '"')
# 用大括号包裹所有的对象
data = '{' + data + '}'
# 转换为JSON格式
json_data = json.loads(data)
# 获取json_data中版本号排序后的最后一个版本号
get_Latest_version = sorted(json_data.keys(), key=lambda x: tuple(map(int, x.split('.'))))[-1]
key_netease = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\MCLauncher')
netease_path = winreg.QueryValueEx(key_netease, "InstallLocation")[0]
netease_version = get_file_version(f"{netease_path}\\WPFLauncher.exe")
if netease_version == get_Latest_version:
    print("当前启动器版本为最新版,无需更新")
else:
    get_uqdate_content = requests.get(f"https://x19.update.netease.com/MCUpdate_{str(get_Latest_version).split('.')[0]}.{str(get_Latest_version).split('.')[1]}.{str(get_Latest_version).split('.')[2]}.txt",headers=headers,verify=False).content.decode("gbk")
    print(f"当前启动器版本为:{netease_version},最新版本为:{get_Latest_version},更新内容:\n\n{get_uqdate_content}\n\n")
    print("正在下载最新版本替换包...")
    download_nofilename(json_data[get_Latest_version]['url'],pathx_pyinstaller)
    print("下载完成,正在终止WPFLauncher.exe进程...")
    os.system("taskkill /im WPFLauncher.exe /f")
    os.system("taskkill /im WPFLauncher.exe /f")
    print(f"完成下载,正在解压文件至:{netease_path}目录下")
    with SevenZipFile(f"{pathx_pyinstaller}\\{os.path.basename(json_data[get_Latest_version]['url'])}", 'r') as archive:
        archive.extractall(path=netease_path)
        print("完成,正在启动游戏")

"""if netease_version != "1.13.2.35313":
    print(f"当前网易我的世界版本:{str(netease_version)}\n最后一个没有发烧平台的网易我的世界版本:1.13.2.35313\n正在下载替换包版本:1.13.2.35313")
    get_netease_patch_url = "https://x19.gph.netease.com/patch1.13.2.35313.X19.Release.7z"
    download_nofilename(get_netease_patch_url,pathx_pyinstaller)
    print("正在终止WPFLauncher.exe进程...")
    os.system("taskkill /im WPFLauncher.exe /f")
    os.system("taskkill /im WPFLauncher.exe /f")
    print(f"完成下载,正在解压文件至:{netease_path}目录下")
    with SevenZipFile(f"{pathx_pyinstaller}\\{os.path.basename(get_netease_patch_url)}", 'r') as archive:
        archive.extractall(path=netease_path)
    print("完成,正在启动游戏")"""
print("终止WPFLauncher.exe进程...")
os.system("taskkill /im WPFLauncher.exe /f")
os.system("taskkill /im WPFLauncher.exe /f")
print("完成,正在启动游戏")
# 定义一个请求处理程序，继承自 SimpleHTTPRequestHandler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # 重写do_GET方法，处理GET请求
    def do_GET(self):
        data_ok = '"$version":{"size": 0, "url": "xxx", "md5": "xxx"},'.replace("$version",str("xxx"))
        # 设置响应状态码为200（表示成功）
        self.send_response(200)
        if self.path == "/pl/x19_java_patchlist":
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(data_ok.encode("gbk"))
            print("发烧平台绕过成功,3秒后自动关闭")
            time.sleep(3)
            with open(r"C:\Windows\System32\drivers\etc\hosts", "r", encoding="utf-8") as f:
                get_hosts = f.read().replace("\n127.0.0.1 x19.update.netease.com", "")
            with open(r"C:\Windows\System32\drivers\etc\hosts", "w", encoding="utf-8") as f:
                f.write(get_hosts)
            sys.exit()
        else:
            try:
                get_ok = json.loads(get_def(f"https://x19.update.netease.com{self.path}"))
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(get_ok,ensure_ascii=False,indent=4).encode("gbk"))
            except Exception:
                get_ok = get_def(f"https://x19.update.netease.com{self.path}")
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(get_ok.encode("gbk"))

# 定义服务器证书和密钥的路径
server_cert = f"{pathx_pyinstaller}\\server.crt"
server_key = f"{pathx_pyinstaller}\\server.key"
# 创建一个SSL上下文，用于客户端认证
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# 使用证书和密钥文件初始化SSL上下文
ssl_context.load_cert_chain(certfile=server_cert, keyfile=server_key)
# 打印重新获取启动器信息
print("重新获取启动器信息...")
# 打开客户端注册表键值
key_netease = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\MCLauncher')
# 获取客户端安装位置
netease_path = winreg.QueryValueEx(key_netease, "InstallLocation")[0]
# 获取客户端版本
netease_version = get_file_version(f"{netease_path}\\WPFLauncher.exe")
# 打印获取完成,启动器版本
print(f"获取完成,启动器版本:{netease_version}")
# 创建 HTTP 服务器，监听本地的443端口（HTTPS 默认端口）
print('请不要直接点击右上角的"X"按钮退出,这很有可能会导致你的启动器无法接收到更新导致出现"网络信号不佳"的情况\n正确的退出做法是在此命令行窗口下按下Ctrl+C\n如果你点了右上角的"X"按钮退出,那么你需要打开此文件:C:\\Windows\\System32\\drivers\\etc\\hosts,然后删除此项\n127.0.0.1 x19.update.netease.com')
print("下面是绕过程序所产生的日志:")
with open(r"C:\Windows\System32\drivers\etc\hosts", "a+", encoding="utf-8") as f:
    f.write("\n127.0.0.1 x19.update.netease.com")
os.startfile(f'{netease_path}\\WPFLauncher.exe')
with socketserver.TCPServer(('localhost', 443), MyHandler) as httpd:
    # 将服务器设置为支持 HTTPS
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    # 启动 HTTPS 服务器，一直运行直到手动终止
    httpd.serve_forever()
