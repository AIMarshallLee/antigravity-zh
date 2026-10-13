#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity 简体中文编程套件 - 命令行入口 (CLI)
命令行工具，一键配置、诊断与辅助 Antigravity 全中文开发
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Windows GBK 终端防乱码与防崩溃处理
if sys.platform == "win32":
    try:
        if sys.stdout.encoding != "utf-8":
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr.encoding != "utf-8":
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 将 core 目录加入 import 路径
CURRENT_DIR = Path(__file__).resolve().parent
CORE_DIR = CURRENT_DIR / "core"
sys.path.insert(0, str(CORE_DIR))

from autostart import AutoStartManager
from configurator import AntigravityConfigurator
from translator import ChineseProgrammingHelper

def print_header():
    print("=" * 64)
    print("🚀 Antigravity 简体中文编程套件 (Antigravity-ZH Toolkit)")
    print("   致力于为 Antigravity 开发者提供极致的简体中文编程体验")
    print("=" * 64)

def cmd_doctor(configurator: AntigravityConfigurator):
    print("\n🔍 正在体检 Antigravity 简体中文环境...\n")
    report = configurator.run_doctor()

    # 1. IDE 界面语言检查
    ide_info = report["ide_locale"]
    print("【1. Antigravity IDE 界面语言配置】")
    if ide_info["configured"]:
        print("  ✅ IDE 语言已正确设置为简体中文 (zh-cn)")
    else:
        print("  ⚠️  IDE 语言尚未强制锁定为简体中文")
    for f in ide_info.get("files", []):
        mark = "✅" if f["is_zh"] else "❌"
        print(f"     {mark} {f['path']} -> locale: '{f['locale'] or '未指定'}'")

    # 2. Git 中文文件名支持
    print("\n【2. Git 中文文件名转义检测】")
    if report["git_chinese_support"]:
        print("  ✅ Git core.quotepath 已配置为 false (中文文件名正常显示，无八进制转义)")
    else:
        print("  ⚠️  Git core.quotepath 未开启 (中文文件名在终端可能会乱码显示为 \\344\\270...)")
        print("     提示：可运行 'antigravity-zh enable' 自动修复")

    # 3. 终端编码检测
    term_info = report["terminal_encoding"]
    print("\n【3. 终端编码与语言环境】")
    if term_info["is_utf8"]:
        print(f"  ✅ 终端采用 UTF-8 编码: LANG={term_info['LANG']}")
    else:
        print(f"  ⚠️  终端编码可能不是 UTF-8: LANG={term_info['LANG']}")

    # 4. 守护进程状态
    manager = AutoStartManager()
    installed = manager.is_installed()
    running = manager.is_running()
    print("\n【4. Antigravity 界面实时汉化自动保活守护】")
    print(f"  - 守护配置已安装: {'✅ 是' if installed else '❌ 否'}")
    print(f"  - 后台进程运行中: {'✅ 是' if running else '❌ 否'}")

    print("\n" + "=" * 64)
    print("💡 建议：可随时运行 'antigravity-zh ui' 立即为正在运行的 Antigravity 窗口注入汉化。")
    print("=" * 64 + "\n")

def cmd_ui(args):
    print("\n🖥️ 正在为 Antigravity 界面注入实时简体中文汉化补丁...\n")
    inject_script = CORE_DIR / "inject.js"
    try:
        res = subprocess.run(["node", str(inject_script)], capture_output=True, text=True, timeout=10)
        print(res.stdout)
        if res.returncode == 0:
            print("🎉 Antigravity 界面已实时汉化成功！请观察左侧栏与主界面。")
        else:
            if res.stderr:
                print(res.stderr)
            print("💡 若提示未找到调试端口，请先启动 Antigravity 客户端后再运行此命令。")
    except Exception as e:
        print(f"❌ 注入过程发生错误: {e}")
    print()

def cmd_autostart(args):
    manager = AutoStartManager()
    action = args.action or "status"
    if action == "enable":
        print("\n🚀 正在安装 Antigravity 简体中文自动持久化守护服务...")
        if manager.install():
            print("✅ 安装成功！已配置开机自启与后台自动监听。")
            print("   👉 效果：无论重启电脑、重开 Antigravity，还是软件自动更新版本，均在 1~3 秒内自动保持汉化！\n")
        else:
            print("❌ 安装失败，请检查相关权限。\n")
    elif action == "disable":
        print("\n🛑 正在停止并移除自动持久化守护服务...")
        if manager.uninstall():
            print("✅ 已成功关闭自动守护服务。\n")
        else:
            print("⚠️ 移除服务失败。\n")
    else:
        installed = manager.is_installed()
        running = manager.is_running()
        print("\n📊 Antigravity 简体中文自动守护状态：")
        print(f"   - 守护配置已安装: {'✅ 是' if installed else '❌ 否'}")
        print(f"   - 后台进程运行中: {'✅ 是' if running else '❌ 否'}")
        if not installed:
            print("\n💡 提示：运行 'antigravity-zh autostart enable' 即可一键开启自动保活！\n")
        else:
            print("\n🎉 守护服务运行良好，更新版本后将全自动保持汉化！\n")

def cmd_enable(configurator: AntigravityConfigurator):
    print("\n⚙️ 正在应用 Antigravity 简体中文环境最佳实践配置...\n")
    results = configurator.apply_all()
    for item in results:
        status_icon = "✅" if item["success"] else "⚠️"
        print(f"  {status_icon} {item['action']}")
        print(f"     -> {item['message']}")
    print("\n🎉 基础中文开发环境配置已完成！建议结合 'antigravity-zh ui' 获得完整体验。\n")

def cmd_update():
    print("\n🔄 正在检查并更新 Antigravity-ZH 最新汉化词典...\n")
    repo_dir = CURRENT_DIR
    git_dir = repo_dir / ".git"
    if git_dir.exists():
        try:
            res = subprocess.run(["git", "pull", "--rebase"], cwd=str(repo_dir), capture_output=True, text=True, timeout=15)
            print(res.stdout)
            if res.returncode == 0:
                print("✅ 汉化词典与程序已更新至最新版本！")
                print("⚡ 正在热载入最新词典至 Antigravity...")
                cmd_ui(None)
            else:
                print(f"⚠️ 更新失败: {res.stderr}")
        except Exception as e:
            print(f"❌ 更新异常: {e}")
    else:
        print("💡 当前为独立安装模式，可重新运行安装脚本进行覆盖更新：")
        print("   curl -fsSL https://raw.githubusercontent.com/AIMarshallLee/antigravity-zh/main/install.sh | bash\n")

def main():
    parser = argparse.ArgumentParser(
        prog="antigravity-zh",
        description="Antigravity 简体中文开发增强套件 CLI 工具"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # doctor
    subparsers.add_parser("doctor", help="体检 Antigravity 简体中文开发环境")

    # ui
    subparsers.add_parser("ui", help="立即向 Antigravity 客户端注入实时汉化补丁")

    # update
    subparsers.add_parser("update", help="检查并更新到最新的汉化词典与程序")

    # autostart
    p_auto = subparsers.add_parser("autostart", help="管理开机自启与自动保活守护服务")
    p_auto.add_argument("action", nargs="?", choices=["enable", "disable", "status"], default="status", help="操作选项")

    # enable
    subparsers.add_parser("enable", help="一键应用 Antigravity 中文开发推荐配置")

    args = parser.parse_args()

    print_header()
    configurator = AntigravityConfigurator()

    if args.command == "doctor":
        cmd_doctor(configurator)
    elif args.command == "ui":
        cmd_ui(args)
    elif args.command == "update":
        cmd_update()
    elif args.command == "autostart":
        cmd_autostart(args)
    elif args.command == "enable":
        cmd_enable(configurator)
    else:
        # 默认无参数时显示简要状态并提示
        cmd_doctor(configurator)

if __name__ == "__main__":
    main()
