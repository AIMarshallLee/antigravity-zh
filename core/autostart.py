#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity 简体中文后台守护服务管理模块 (跨平台: macOS LaunchAgent + Windows Startup)
负责配置开机自启动与后台守护，确保应用升级、重启依然 100% 自动保持汉化
"""

import os
import sys
import subprocess
from pathlib import Path

PLIST_NAME = "com.antigravity.zh-daemon.plist"
WIN_TASK_NAME = "AntigravityZH-Daemon"
WIN_VBS_NAME = "AntigravityZH-Daemon.vbs"

class AutoStartManager:
    """跨平台 (macOS / Windows) 自动化守护管理器"""

    def __init__(self):
        self.is_windows = sys.platform == "win32"
        self.home_dir = Path.home()
        self.script_dir = Path(__file__).parent.resolve()
        self.daemon_script = self.script_dir / "daemon.js"
        self.node_path = self._find_node()

        if self.is_windows:
            appdata = os.environ.get("APPDATA")
            if appdata:
                self.win_startup_dir = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            else:
                self.win_startup_dir = self.home_dir / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            self.win_vbs_path = self.win_startup_dir / WIN_VBS_NAME
        else:
            self.launch_agents_dir = self.home_dir / "Library" / "LaunchAgents"
            self.plist_path = self.launch_agents_dir / PLIST_NAME

    def _find_node(self) -> str:
        """寻找 node 解释器真实路径"""
        if self.is_windows:
            for candidate in [
                os.path.expandvars(r"%ProgramFiles%\nodejs\node.exe"),
                os.path.expandvars(r"%ProgramFiles(x86)%\nodejs\node.exe"),
                os.path.expandvars(r"%LOCALAPPDATA%\Programs\node\node.exe"),
            ]:
                if os.path.exists(candidate):
                    return candidate
            try:
                res = subprocess.run(["where", "node"], capture_output=True, text=True, shell=True)
                if res.returncode == 0 and res.stdout.strip():
                    return res.stdout.strip().splitlines()[0]
            except Exception:
                pass
            return "node"
        else:
            for candidate in ["/usr/local/bin/node", "/opt/homebrew/bin/node", "/usr/bin/node"]:
                if os.path.exists(candidate):
                    return candidate
            try:
                res = subprocess.run(["which", "node"], capture_output=True, text=True)
                if res.returncode == 0 and res.stdout.strip():
                    return res.stdout.strip()
            except Exception:
                pass
            return "node"

    def is_installed(self) -> bool:
        """检查守护服务是否已安装"""
        if self.is_windows:
            return self.win_vbs_path.exists()
        else:
            return self.plist_path.exists()

    def is_running(self) -> bool:
        """检查守护服务是否正在运行"""
        if self.is_windows:
            try:
                # 检查后台是否有 node 正在运行 daemon.js
                cmd = 'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*daemon.js*\' } | Measure-Object | Select-Object -ExpandProperty Count"'
                res = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=5)
                if res.returncode == 0 and res.stdout.strip():
                    return int(res.stdout.strip()) > 0
            except Exception:
                pass
            return False
        else:
            try:
                res = subprocess.run(["launchctl", "list", "com.antigravity.zh-daemon"], capture_output=True, text=True)
                return res.returncode == 0
            except Exception:
                return False

    def install(self) -> bool:
        """安装并启动后台守护服务"""
        if self.is_windows:
            try:
                self.win_startup_dir.mkdir(parents=True, exist_ok=True)
                log_dir = self.home_dir / ".antigravity-zh" / "logs"
                log_dir.mkdir(parents=True, exist_ok=True)

                daemon_path_str = str(self.daemon_script).replace("\\", "\\\\")
                node_path_str = str(self.node_path).replace("\\", "\\\\")

                # 生成纯静默无黑框且自动崩溃重启的 VBScript 守护看门狗
                vbs_content = (
                    'Set WshShell = CreateObject("WScript.Shell")\r\n'
                    'Do\r\n'
                    f'  WshShell.Run """{node_path_str}"" ""{daemon_path_str}""", 0, True\r\n'
                    '  WScript.Sleep 3000\r\n'
                    'Loop\r\n'
                )
                self.win_vbs_path.write_text(vbs_content, encoding="utf-8")

                # 双重保障：注册 Windows 注册表开机自启 (当前用户无需管理员权限，100% 成功)
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
                    winreg.SetValueEx(key, "AntigravityZHDaemon", 0, winreg.REG_SZ, f'wscript.exe "{self.win_vbs_path}"')
                    winreg.CloseKey(key)
                except Exception:
                    pass

                # 终止旧的守护进程与看门狗
                try:
                    kill_cmd = 'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*daemon.js*\' -or $_.CommandLine -like \'*AntigravityZH-Daemon*\' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"'
                    subprocess.run(kill_cmd, capture_output=True, shell=True)
                except Exception:
                    pass

                # 立即在后台静默启动看门狗守护
                subprocess.Popen(
                    ["wscript.exe", str(self.win_vbs_path)],
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                    shell=True
                )
                return True
            except Exception as e:
                print(f"⚠️ 注册 Windows 启动服务失败: {e}")
                return False
        else:
            self.launch_agents_dir.mkdir(parents=True, exist_ok=True)
            log_dir = self.home_dir / "Library" / "Logs" / "AntigravityZH"
            log_dir.mkdir(parents=True, exist_ok=True)

            stdout_log = str(log_dir / "daemon.log")
            stderr_log = str(log_dir / "error.log")

            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.antigravity.zh-daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.node_path}</string>
        <string>{str(self.daemon_script)}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{stdout_log}</string>
    <key>StandardErrorPath</key>
    <string>{stderr_log}</string>
</dict>
</plist>
"""
            self.plist_path.write_text(plist_content, encoding="utf-8")

            # 卸载旧的并加载新的
            try:
                subprocess.run(["launchctl", "unload", str(self.plist_path)], capture_output=True)
                subprocess.run(["launchctl", "load", str(self.plist_path)], check=True, capture_output=True)
                return True
            except Exception as e:
                print(f"⚠️ 加载 launchctl 失败: {e}")
                return False

    def uninstall(self) -> bool:
        """停止并移除后台守护服务"""
        if self.is_windows:
            try:
                if self.win_vbs_path.exists():
                    self.win_vbs_path.unlink()
                # 移除注册表自启项与任务计划
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
                    winreg.DeleteValue(key, "AntigravityZHDaemon")
                    winreg.CloseKey(key)
                except Exception:
                    pass
                try:
                    subprocess.run(["schtasks", "/delete", "/tn", WIN_TASK_NAME, "/f"], capture_output=True, shell=True)
                except Exception:
                    pass
                # 终止正在运行的 daemon 进程与看门狗
                cmd = 'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*daemon.js*\' -or $_.CommandLine -like \'*AntigravityZH-Daemon*\' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"'
                subprocess.run(cmd, capture_output=True, shell=True)
                return True
            except Exception:
                return False
        else:
            if self.plist_path.exists():
                try:
                    subprocess.run(["launchctl", "unload", str(self.plist_path)], capture_output=True)
                    self.plist_path.unlink()
                    return True
                except Exception:
                    return False
            return True
