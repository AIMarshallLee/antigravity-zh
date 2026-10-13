#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity 简体中文环境配置管理器
负责检测、配置与修复 Antigravity IDE 及操作系统的中文编程开发环境
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Tuple, List

class AntigravityConfigurator:
    """Antigravity 中文环境诊断与配置核心类"""

    def __init__(self):
        self.home_dir = Path.home()
        self.ide_argv_paths = [
            self.home_dir / ".antigravity-ide" / "argv.json",
            self.home_dir / ".antigravity" / "argv.json"
        ]
        if os.name == 'nt' or sys.platform == 'win32':
            appdata = os.environ.get("APPDATA")
            appdata_path = Path(appdata) if appdata else self.home_dir / "AppData" / "Roaming"
            self.settings_paths = [
                appdata_path / "Antigravity IDE" / "User" / "settings.json",
                appdata_path / "Antigravity" / "User" / "settings.json",
                appdata_path / "antigravity" / "User" / "settings.json",
            ]
        else:
            self.settings_paths = [
                self.home_dir / "Library/Application Support/Antigravity IDE/User/settings.json",
                self.home_dir / "Library/Application Support/Antigravity/User/settings.json"
            ]

    def _read_json_with_comments(self, file_path: Path) -> Tuple[Dict[str, Any], str]:
        """读取可能包含注释的 JSON 文件，保留原始文本格式"""
        if not file_path.exists():
            return {}, ""
        try:
            content = file_path.read_text(encoding="utf-8")
            # 简单清洗注释用于解析
            cleaned_lines = []
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("/*") or stripped.endswith("*/"):
                    continue
                cleaned_lines.append(line)
            cleaned_content = "\n".join(cleaned_lines)
            data = json.loads(cleaned_content)
            return data, content
        except Exception:
            return {}, ""

    def _check_file_locale(self, file_path: Path) -> Tuple[bool, str]:
        """检查文件中是否配置了 zh-cn"""
        if not file_path.exists():
            return False, ""
        try:
            content = file_path.read_text(encoding="utf-8")
            import re
            match = re.search(r'"locale"\s*:\s*"([^"]+)"', content)
            if match:
                val = match.group(1).lower()
                return val in ["zh-cn", "zh-hans"], val
            return False, ""
        except Exception:
            return False, ""

    def check_ide_locale(self) -> Dict[str, Any]:
        """检查 Antigravity IDE argv.json 中的语言配置"""
        status = {"configured": False, "files": []}
        all_configured = True
        found_any = False

        for path in self.ide_argv_paths:
            if path.exists():
                found_any = True
                is_zh, locale_val = self._check_file_locale(path)
                status["files"].append({
                    "path": str(path),
                    "locale": locale_val,
                    "is_zh": is_zh
                })
                if not is_zh:
                    all_configured = False

        status["configured"] = found_any and all_configured
        return status

    def fix_ide_locale(self) -> List[str]:
        """一键将 Antigravity argv.json 语言更新为 zh-cn"""
        modified = []
        for path in self.ide_argv_paths:
            if not path.parent.exists():
                continue
            
            data = {}
            if path.exists():
                try:
                    # 尝试保留原有 JSON 结构
                    content = path.read_text(encoding="utf-8")
                    lines = content.splitlines()
                    # 查找是否已有 "locale"
                    has_locale = any('"locale"' in line for line in lines)
                    if has_locale:
                        new_lines = []
                        for line in lines:
                            if '"locale"' in line:
                                new_lines.append('\t"locale": "zh-cn",')
                            else:
                                new_lines.append(line)
                        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                        modified.append(str(path))
                        continue
                    else:
                        # 插入到首个大括号后面
                        for i, line in enumerate(lines):
                            if "{" in line:
                                lines.insert(i + 1, '\t"locale": "zh-cn",')
                                break
                        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                        modified.append(str(path))
                        continue
                except Exception:
                    pass

            # 若文件不存在或写入异常，创建标准配置
            data = {"locale": "zh-cn", "enable-crash-reporter": True}
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            modified.append(str(path))

        return modified

    def check_git_chinese_support(self) -> bool:
        """检查 Git 是否开启了中文路径不转义配置 (core.quotepath false)"""
        try:
            res = subprocess.run(
                ["git", "config", "--global", "--get", "core.quotepath"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return res.stdout.strip() == "false"
        except Exception:
            return False

    def fix_git_chinese_support(self) -> bool:
        """配置 Git 全局支持中文文件名直接显示"""
        try:
            subprocess.run(
                ["git", "config", "--global", "core.quotepath", "false"],
                check=True,
                timeout=5
            )
            subprocess.run(
                ["git", "config", "--global", "gui.encoding", "utf-8"],
                check=True,
                timeout=5
            )
            subprocess.run(
                ["git", "config", "--global", "i18n.commitencoding", "utf-8"],
                check=True,
                timeout=5
            )
            subprocess.run(
                ["git", "config", "--global", "i18n.logoutputencoding", "utf-8"],
                check=True,
                timeout=5
            )
            return True
        except Exception:
            return False

    def check_terminal_encoding(self) -> Dict[str, str]:
        """检查终端语言与编码环境"""
        return {
            "LANG": os.environ.get("LANG", "未设置"),
            "LC_ALL": os.environ.get("LC_ALL", "未设置"),
            "is_utf8": "UTF-8" in os.environ.get("LANG", "").upper()
        }

    def run_doctor(self) -> Dict[str, Any]:
        """全面诊断 Antigravity 中文开发环境"""
        ide_locale = self.check_ide_locale()
        git_zh = self.check_git_chinese_support()
        term = self.check_terminal_encoding()

        # 检查当前工作区或用户目录下的规则与技能扩展
        cwd = Path.cwd()
        workspace_rule = cwd / ".agent" / "rules" / "chinese-programming.md"
        skill_doc = self.home_dir / ".gemini" / "antigravity" / "skills" / "antigravity-zh" / "SKILL.md"

        return {
            "ide_locale": ide_locale,
            "git_chinese_support": git_zh,
            "terminal_encoding": term,
            "chinese_rule_installed": workspace_rule.exists(),
            "chinese_skill_installed": skill_doc.exists(),
        }

    def apply_all(self) -> List[Dict[str, Any]]:
        """应用全部中文环境推荐配置"""
        results = []
        mod_files = self.fix_ide_locale()
        check_status = self.check_ide_locale()

        if mod_files:
            ide_msg = f"已生效: {', '.join(mod_files)}"
            ide_ok = True
        elif check_status.get("configured"):
            ide_msg = "已是 zh-cn 配置"
            ide_ok = True
        else:
            ide_msg = "未检测到 Antigravity IDE 配置目录，已跳过"
            ide_ok = False

        results.append({
            "action": "IDE 界面语言配置 (zh-cn)",
            "success": ide_ok,
            "message": ide_msg
        })
        git_ok = self.fix_git_chinese_support()
        results.append({
            "action": "Git 中文路径转义与 UTF-8 编码 (core.quotepath false)",
            "success": git_ok,
            "message": "已开启 Git 中文文件名友好显示" if git_ok else "Git 配置未执行成功"
        })
        return results
