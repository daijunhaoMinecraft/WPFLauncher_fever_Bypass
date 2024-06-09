import http.server
import json
import socketserver
import ssl
import sys
import threading
import time
import winreg
import os
import win32api
import requests,certifi
from urllib.parse import urlparse
from tqdm.rich import tqdm
from py7zr import SevenZipFile
import psutil
import warnings
warnings.simplefilter("ignore")
import atexit
@atexit.register
def atexit_fun():
    with open(r"C:\Windows\System32\drivers\etc\hosts", "r", encoding="utf-8") as f:
        get_hosts = f.read().replace("\n127.0.0.1 x19.update.netease.com", "")
    with open(r"C:\Windows\System32\drivers\etc\hosts", "w", encoding="utf-8") as f:
        f.write(get_hosts)

def find_process_by_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if conn.laddr.port == port:
                    return proc
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
    reset_connect = 1
    while True:
        try:
            download_file = requests.get(url,headers=headers,verify=certifi.where(),stream=True)
            break
        except Exception:
            print("下载失败,正在重新下载,重连次数:")
            reset_connect += 1
    download_file_size = int(download_file.headers['Content-Length'])/1024
    file_name = os.path.basename(urlparse(url).path)
    with open(file=f"{save}\\{file_name}", mode="wb") as f:
        for data in tqdm(iterable=download_file.iter_content(1024),total=download_file_size,unit='KB',desc=f"正在下载文件:{file_name}"):
            f.write(data)
def get_def(url):
    with open(r"C:\Windows\System32\drivers\etc\hosts", "r", encoding="utf-8") as f:
        get_hosts = f.read().replace("\n127.0.0.1 x19.update.netease.com", "")
        f.close()
    with open(r"C:\Windows\System32\drivers\etc\hosts", "w", encoding="utf-8") as f:
        f.write(get_hosts)
        f.close()
    get_content = requests.get(url,headers={"Host": "x19.update.netease.com"},verify=certifi.where()).text
    with open(r"C:\Windows\System32\drivers\etc\hosts", "a+", encoding="utf-8") as f:
        f.write("\n127.0.0.1 x19.update.netease.com")
    return get_content

#获取当前执行exe的路径
pathx_pyinstaller = os.path.dirname(os.path.realpath(sys.argv[0]))
def get_file_version(file_path):
    try:
        info = win32api.GetFileVersionInfo(file_path, '\\')
        return '{0}.{1}.{2}.{3}'.format(
            info['FileVersionMS'] >> 16,
            info['FileVersionMS'] & 0xFFFF,
            info['FileVersionLS'] >> 16,
            info['FileVersionLS'] & 0xFFFF
        )
    except Exception as e:
        print("Error:", e)
        return None
try:
    key_netease = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\MCLauncher')
    netease_path = winreg.QueryValueEx(key_netease, "InstallLocation")[0]
    netease_version = get_file_version(f"{netease_path}\\WPFLauncher.exe")
except Exception as e:
    print(e)
    input()
    sys.exit()
if netease_version != "1.13.2.35313":
    print(f"当前网易我的世界版本:{str(netease_version)}\n最后一个没有发烧平台的网易我的世界版本:1.13.2.35313\n正在下载替换包版本:1.13.2.35313")
    get_netease_patch_url = "https://x19.gph.netease.com/patch1.13.2.35313.X19.Release.7z"
    download_nofilename(get_netease_patch_url,pathx_pyinstaller)
    print("正在终止WPFLauncher.exe进程...")
    os.system("taskkill /im WPFLauncher.exe /f")
    os.system("taskkill /im WPFLauncher.exe /f")
    print(f"完成下载,正在解压文件至:{netease_path}目录下")
    with SevenZipFile(f"{pathx_pyinstaller}\\{os.path.basename(get_netease_patch_url)}", 'r') as archive:
        archive.extractall(path=netease_path)
    print("完成,正在启动游戏")
print("正在检测端口占用情况")
port = 443
process = find_process_by_port(port)
if process:
    kill_process(process)
else:
    print(f"恭喜,未发现443端口被占用的情况")
print("端口占用检测完成,正在启动游戏...")
# 定义一个请求处理程序，继承自 SimpleHTTPRequestHandler
class MyHandler(http.server.SimpleHTTPRequestHandler):
    # 重写do_GET方法，处理GET请求
    def do_GET(self):
        data_ok = '"$version":{"size": 0, "url": "xxx", "md5": "xxx"},'.replace("$version",str(netease_version))
        # 设置响应状态码为200（表示成功）
        self.send_response(200)
        if self.path == "/pl/x19_java_patchlist":
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(data_ok.encode("gbk"))

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

server_cert = f"{pathx_pyinstaller}\\server.crt"
server_key = f"{pathx_pyinstaller}\\server.key"
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=server_cert, keyfile=server_key)
print("重新获取启动器信息...")
key_netease = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Netease\MCLauncher')
netease_path = winreg.QueryValueEx(key_netease, "InstallLocation")[0]
netease_version = get_file_version(f"{netease_path}\\WPFLauncher.exe")
print(f"获取完成,启动器版本:{netease_version}")
# 创建 HTTP 服务器，监听本地的443端口（HTTPS 默认端口）
print('请不要直接点击右上角的"X"按钮退出,这很有可能会导致你的启动器无法接收到更新导致出现"网络信号不佳"的情况\n正确的退出做法是在此命令行窗口下按下Ctrl+C\n如果你点了右上角的"X"按钮退出,那么你需要打开此文件:C:\\Windows\\System32\\drivers\\etc\\hosts,然后删除此项\n127.0.0.1 x19.update.netease.com')
print("下面是绕更新程序所产生的日志:")
with open(r"C:\Windows\System32\drivers\etc\hosts", "a+", encoding="utf-8") as f:
    f.write("\n127.0.0.1 x19.update.netease.com")
os.startfile(f'{netease_path}\\WPFLauncher.exe')
with socketserver.TCPServer(('localhost', 443), MyHandler) as httpd:
    # 将服务器设置为支持 HTTPS
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    # 启动 HTTPS 服务器，一直运行直到手动终止
    httpd.serve_forever()