#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity 简体中文后台守护服务管理模块 (macOS LaunchAgent)
负责配置开机自启动与后台守护，确保应用升级、重启依然 100% 自动保持汉化
"""

import os
import subprocess
from pathlib import Path

PLIST_NAME = "com.antigravity.zh-daemon.plist"

class AutoStartManager:
    """macOS LaunchAgent 自动化守护管理器"""

    def __init__(self):
        self.home_dir = Path.home()
        self.launch_agents_dir = self.home_dir / "Library" / "LaunchAgents"
        self.plist_path = self.launch_agents_dir / PLIST_NAME
        self.script_dir = Path(__file__).parent.resolve()
        self.daemon_script = self.script_dir / "daemon.js"
        self.node_path = self._find_node()

    def _find_node(self) -> str:
        """寻找 node 解释器真实路径"""
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
        return self.plist_path.exists()

    def is_running(self) -> bool:
        """检查守护服务是否正在运行"""
        try:
            res = subprocess.run(["launchctl", "list", "com.antigravity.zh-daemon"], capture_output=True, text=True)
            return res.returncode == 0
        except Exception:
            return False

    def install(self) -> bool:
        """安装并启动后台守护服务"""
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
        if self.plist_path.exists():
            try:
                subprocess.run(["launchctl", "unload", str(self.plist_path)], capture_output=True)
                self.plist_path.unlink()
                return True
            except Exception:
                return False
        return True
