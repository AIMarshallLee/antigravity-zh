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

                # 生成纯静默无黑框 VBScript 启动桥
                vbs_content = f'Set WshShell = CreateObject("WScript.Shell")\r\nWshShell.Run """{node_path_str}"" ""{daemon_path_str}""", 0, False\r\n'
                self.win_vbs_path.write_text(vbs_content, encoding="utf-8")

                # 立即在后台静默启动一次守护进程
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

            # 安装启动参数包装器，保证任何途径启动 Antigravity 都带 --remote-debugging-port=0
            self._ensure_mac_wrapper()

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
                # 终止正在运行的 daemon 进程
                cmd = 'powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*daemon.js*\' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"'
                subprocess.run(cmd, capture_output=True, shell=True)
                return True
            except Exception:
                return False
        else:
            if self.plist_path.exists():
                try:
                    subprocess.run(["launchctl", "unload", str(self.plist_path)], capture_output=True)
                    self.plist_path.unlink()
                except Exception:
                    pass
            self._restore_mac_wrapper()
            return True

    def _ensure_mac_wrapper(self):
        """为 macOS Antigravity.app 安装自启调试参数包装脚本"""
        try:
            macos_dir = Path("/Applications/Antigravity.app/Contents/MacOS")
            main_bin = macos_dir / "Antigravity"
            real_bin = macos_dir / "Antigravity.bin"

            if not main_bin.exists():
                return

            with open(main_bin, "rb") as f:
                header = f.read(4)

            if not header.startswith(b"#!"):
                import shutil
                shutil.copy2(main_bin, real_bin)
                real_bin.chmod(0o755)

                wrapper = '#!/bin/bash\nDIR="$(cd "$(dirname "$0")" && pwd)"\nexec "$DIR/Antigravity.bin" --remote-debugging-port=0 "$@"\n'
                main_bin.write_text(wrapper, encoding="utf-8")
                main_bin.chmod(0o755)
        except Exception as e:
            print(f"⚠️ 安装 macOS 启动包装器跳过: {e}")

    def _restore_mac_wrapper(self):
        """恢复 macOS Antigravity.app 原始二进制"""
        try:
            macos_dir = Path("/Applications/Antigravity.app/Contents/MacOS")
            main_bin = macos_dir / "Antigravity"
            real_bin = macos_dir / "Antigravity.bin"

            if real_bin.exists():
                real_bin.replace(main_bin)
                main_bin.chmod(0o755)
        except Exception:
            pass
