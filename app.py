#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
Antigravity-ZH: 谷歌 Antigravity 官方级全界面简体中文套件 (统一零依赖独立引擎)
GitHub: https://github.com/AIMarshallLee/antigravity-zh
作者: 昆仑增长团队 (Kunlun Growth)

架构特性：
1. 100% 纯 Python 标准库开发，完全零第三方依赖 (零 urllib3 / 零 websockets / 零 requests)
2. 内置原生纯 Python WebSocket (RFC 6455) 极轻量客户端，毫秒级直通 CDP 调试协议
3. 支持 PyInstaller 一键编译为单文件零依赖二进制 (.exe / macOS 可执行程序 / .dmg)
4. 支持双击图形交互引导 (小白模式) 与命令行静默参数 (极客守护模式)
==============================================================================
"""

import os
import sys
import time
import json
import socket
import urllib.parse
import urllib.request
import subprocess
import threading
from pathlib import Path

VERSION = "v1.0.0"

# ==============================================================================
# 1. 内嵌注入脚本加载器
# ==============================================================================
def get_injector_script() -> str:
    """获取 JavaScript 注入脚本代码"""
    # 优先读取本地 core/injector.js
    local_path = Path(__file__).parent / "core" / "injector.js"
    if local_path.exists():
        try:
            return local_path.read_text(encoding="utf-8")
        except Exception:
            pass
    
    # 打包为 PyInstaller 单文件时，从临时解压目录读取
    if hasattr(sys, "_MEIPASS"):
        meipass_path = Path(sys._MEIPASS) / "core" / "injector.js"
        if meipass_path.exists():
            return meipass_path.read_text(encoding="utf-8")

    return ""

# ==============================================================================
# 2. 全平台 DevToolsActivePort 端口探测器
# ==============================================================================
def find_devtools_port() -> int:
    """跨平台寻找 Antigravity 的 Chromium 远程调试端口"""
    home = Path.home()
    possible_paths = []

    if sys.platform == "win32":
        local_appdata = os.environ.get("LOCALAPPDATA", str(home / "AppData" / "Local"))
        appdata = os.environ.get("APPDATA", str(home / "AppData" / "Roaming"))
        user_profile = os.environ.get("USERPROFILE", str(home))

        possible_paths.extend([
            Path(local_appdata) / "Chromium" / "DevToolsActivePort",
            Path(local_appdata) / "Chromium" / "User Data" / "DevToolsActivePort",
            Path(local_appdata) / "Antigravity" / "DevToolsActivePort",
            Path(local_appdata) / "Antigravity" / "User Data" / "DevToolsActivePort",
            Path(local_appdata) / "antigravity" / "DevToolsActivePort",
            Path(appdata) / "Chromium" / "DevToolsActivePort",
            Path(appdata) / "Antigravity" / "DevToolsActivePort",
            Path(appdata) / "antigravity" / "DevToolsActivePort",
            Path(user_profile) / ".antigravity" / "DevToolsActivePort",
        ])
    elif sys.platform == "darwin":
        possible_paths.extend([
            home / "Library" / "Application Support" / "Chromium" / "DevToolsActivePort",
            home / "Library" / "Application Support" / "Antigravity" / "DevToolsActivePort",
            home / "Library" / "Application Support" / "antigravity" / "DevToolsActivePort",
        ])
    else:
        possible_paths.extend([
            home / ".config" / "chromium" / "DevToolsActivePort",
            home / ".config" / "antigravity" / "DevToolsActivePort",
        ])

    for p in possible_paths:
        if p.exists():
            try:
                lines = p.read_text(encoding="utf-8").strip().splitlines()
                if lines:
                    port = int(lines[0].strip())
                    if port > 0:
                        return port
            except Exception:
                continue

    return 0

# ==============================================================================
# 3. 极轻量纯原生 Python WebSocket CDP 协议客户端 (RFC 6455)
# ==============================================================================
class PurePythonWebSocketClient:
    """仅依赖 Python 标准库 socket 的极轻量 WebSocket 客户端"""

    def __init__(self, ws_url: str, timeout: float = 3.0):
        self.ws_url = ws_url
        self.timeout = timeout
        self.sock = None

    def connect(self) -> bool:
        parsed = urllib.parse.urlparse(self.ws_url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 80
        path = parsed.path or "/"

        self.sock = socket.create_connection((host, port), timeout=self.timeout)

        # 构造握手报文
        handshake = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode("utf-8"))

        # 接收握手回应
        resp = self.sock.recv(4096).decode("utf-8", errors="ignore")
        return "101" in resp

    def send_text(self, text: str):
        payload = text.encode("utf-8")
        mask_key = b"\x24\x88\x13\x57"

        # 构造帧头
        frame = bytearray([0x81])  # FIN + Text frame
        length = len(payload)
        if length <= 125:
            frame.append(0x80 | length)
        elif length <= 65535:
            frame.append(0x80 | 126)
            frame.extend(length.to_bytes(2, "big"))
        else:
            frame.append(0x80 | 127)
            frame.extend(length.to_bytes(8, "big"))

        frame.extend(mask_key)
        masked = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))
        frame.extend(masked)

        self.sock.sendall(frame)

    def recv_text(self) -> str:
        try:
            data = self.sock.recv(65536)
            if not data or len(data) < 2:
                return ""
            payload_len = data[1] & 0x7F
            idx = 2
            if payload_len == 126:
                idx = 4
            elif payload_len == 127:
                idx = 10
            return data[idx:].decode("utf-8", errors="ignore")
        except Exception:
            return ""

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None

# ==============================================================================
# 4. CDP 注入与守护核心业务逻辑
# ==============================================================================
def inject_chinese_into_page(ws_url: str, script_code: str) -> bool:
    """向目标页面注入汉化补丁"""
    client = PurePythonWebSocketClient(ws_url)
    try:
        if not client.connect():
            return False

        # 1. 执行当前页面内存注入
        msg1 = json.dumps({
            "id": 101,
            "method": "Runtime.evaluate",
            "params": {
                "expression": script_code,
                "returnByValue": True
            }
        })
        client.send_text(msg1)
        resp1 = client.recv_text()

        # 2. 注入页面持久化钩子 (页面切换/刷新自动继承)
        msg2 = json.dumps({
            "id": 102,
            "method": "Page.addScriptToEvaluateOnNewDocument",
            "params": {"source": script_code}
        })
        client.send_text(msg2)
        resp2 = client.recv_text()

        return True
    except Exception:
        return False
    finally:
        client.close()

def execute_injection() -> bool:
    """一次性触发界面汉化注入"""
    port = find_devtools_port()
    if not port:
        return False

    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=2)
        targets = json.loads(req.read().decode("utf-8"))
    except Exception:
        return False

    script_code = get_injector_script()
    if not script_code:
        return False

    pages = [t for t in targets if t.get("type") == "page" and "webSocketDebuggerUrl" in t]
    success_count = 0
    for page in pages:
        ws_url = page["webSocketDebuggerUrl"]
        if inject_chinese_into_page(ws_url, script_code):
            success_count += 1

    return success_count > 0

def run_daemon_loop():
    """后台高频保活守护循环 (1秒周期)"""
    script_code = get_injector_script()
    while True:
        try:
            port = find_devtools_port()
            if port:
                req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json", timeout=1)
                targets = json.loads(req.read().decode("utf-8"))
                pages = [t for t in targets if t.get("type") == "page" and "webSocketDebuggerUrl" in t]
                for page in pages:
                    ws_url = page["webSocketDebuggerUrl"]
                    # 检查是否已注入
                    c = PurePythonWebSocketClient(ws_url, timeout=1.0)
                    if c.connect():
                        c.send_text(json.dumps({
                            "id": 99,
                            "method": "Runtime.evaluate",
                            "params": {"expression": "!!window.__ANTIGRAVITY_ZH_INJECTED__", "returnByValue": True}
                        }))
                        r = c.recv_text()
                        if '"value":true' not in r:
                            inject_chinese_into_page(ws_url, script_code)
                        c.close()
        except Exception:
            pass
        time.sleep(1.0)

# ==============================================================================
# 5. 开机自启守护配置
# ==============================================================================
def enable_autostart() -> bool:
    """开启系统开机自启动与后台守护"""
    home = Path.home()
    if sys.platform == "win32":
        try:
            appdata = os.environ.get("APPDATA", str(home / "AppData" / "Roaming"))
            startup_dir = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            startup_dir.mkdir(parents=True, exist_ok=True)
            vbs_file = startup_dir / "AntigravityZH-Daemon.vbs"

            # 如果当前是打包好的 exe
            if getattr(sys, "frozen", False):
                exe_path = sys.executable.replace("\\", "\\\\")
                vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\r\nWshShell.Run """{exe_path}"" --daemon", 0, False\r\n'
            else:
                py_path = sys.executable.replace("\\", "\\\\")
                script_path = str(Path(__file__).resolve()).replace("\\", "\\\\")
                vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\r\nWshShell.Run """{py_path}"" ""{script_path}"" --daemon", 0, False\r\n'

            vbs_file.write_text(vbs_content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"配置 Windows 启动项失败: {e}")
            return False
    elif sys.platform == "darwin":
        try:
            agents_dir = home / "Library" / "LaunchAgents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            plist_file = agents_dir / "com.antigravity.zh-daemon.plist"

            if getattr(sys, "frozen", False):
                args_xml = f"<string>{sys.executable}</string>\n        <string>--daemon</string>"
            else:
                args_xml = f"<string>{sys.executable}</string>\n        <string>{str(Path(__file__).resolve())}</string>\n        <string>--daemon</string>"

            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.antigravity.zh-daemon</string>
    <key>ProgramArguments</key>
    <array>
        {args_xml}
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
"""
            plist_file.write_text(plist_content, encoding="utf-8")
            subprocess.run(["launchctl", "unload", str(plist_file)], capture_output=True)
            subprocess.run(["launchctl", "load", str(plist_file)], check=True, capture_output=True)
            return True
        except Exception as e:
            print(f"配置 macOS LaunchAgent 失败: {e}")
            return False
    return False

# ==============================================================================
# 6. 小白双击 GUI / 控制台交互界面
# ==============================================================================
def run_interactive_wizard():
    """小白双击直接运行的交互式引导向导"""
    os.system("cls" if sys.platform == "win32" else "clear")
    print("=" * 66)
    print("   🚀 Antigravity-ZH: 谷歌 Antigravity 全界面高精汉化套件")
    print("   版本: " + VERSION + " | 架构: 零依赖单文件版 | 维护: 昆仑增长团队")
    print("=" * 66)
    print("")

    # 1. 尝试检测与热汉化
    print("🔍 [1/3] 正在检测系统中的 Antigravity 运行状态...")
    port = find_devtools_port()
    if port:
        print(f"  ✓ 成功检测到 Antigravity 正在运行 (调试端口: {port})")
        print("⚡ [2/3] 正在执行全界面简体中文热注入...")
        if execute_injection():
            print("  🎉 恭喜！当前 Antigravity 界面已即刻完成 100% 简体中文汉化！")
        else:
            print("  ⚠️ 注入指令已下发，请切回 Antigravity 窗口观察界面变化。")
    else:
        print("  💡 提示：当前未检测到正在运行的 Antigravity 客户端。")
        print("  ✓ 无需担心，安装后台守护后，每次打开软件均会自动秒级汉化！")

    # 2. 开启后台自愈守护
    print("")
    print("🛡️ [3/3] 正在配置系统级开机自愈守护 (升级、重启、新建会话均自动保持汉化)...")
    if enable_autostart():
        print("  ✓ 系统守护已成功启用！彻底告别回滚英文。")
    else:
        print("  ⚠️ 守护配置跳过，当前已完成单次注入。")

    print("")
    print("=" * 66)
    print("   🌟 全部就绪！现在请直接打开或切回 Antigravity 畅享中文编程体验！")
    print("   💬 官方社群：欢迎加入飞书「昆仑增长 AI 交流群」（详见 GitHub 首页）")
    print("=" * 66)
    print("")
    input("👉 按回车键 (Enter) 退出安装程序...")

# ==============================================================================
# 7. 主程序入口
# ==============================================================================
def main():
    args = sys.argv[1:]

    # 守护进程模式
    if "--daemon" in args:
        run_daemon_loop()
        return

    # 命令行单次热注入
    if "--ui" in args or "ui" in args:
        if execute_injection():
            print("✅ Antigravity 界面汉化已即刻生效！")
        else:
            print("❌ 未检测到 Antigravity 运行端口，请先启动软件。")
        return

    # 命令行开启守护
    if "autostart" in args and "enable" in args:
        if enable_autostart():
            print("✅ 后台守护服务已成功配置！")
        else:
            print("❌ 配置失败。")
        return

    # 默认模式：双击或无参数运行 -> 启动小白交互式向导
    run_interactive_wizard()

if __name__ == "__main__":
    main()
