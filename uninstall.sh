#!/usr/bin/env bash
# ==============================================================================
#  Antigravity-ZH 一键干净卸载脚本
# ==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${YELLOW}${BOLD}正在为您干净卸载 Antigravity-ZH 简体中文套件...${NC}"

INSTALL_DIR="$HOME/.antigravity-zh"

# 1. 停止并移除 LaunchAgent
if [ -f "$INSTALL_DIR/cli.py" ]; then
    python3 "$INSTALL_DIR/cli.py" autostart disable >/dev/null 2>&1 || true
fi
launchctl unload "$HOME/Library/LaunchAgents/com.antigravity.zh-daemon.plist" 2>/dev/null || true
rm -f "$HOME/Library/LaunchAgents/com.antigravity.zh-daemon.plist"
rm -rf "$HOME/Library/Logs/AntigravityZH"
echo -e "${GREEN}  ✓ 已停止并清除后台守护进程与日志${NC}"

# 2. 移除全局命令软链接
rm -f "/usr/local/bin/antigravity-zh"
rm -f "$HOME/.local/bin/antigravity-zh"
echo -e "${GREEN}  ✓ 已移除命令行软链接 (antigravity-zh)${NC}"

# 3. 移除安装目录
rm -rf "$INSTALL_DIR"
echo -e "${GREEN}  ✓ 已清理安装文件目录 ($INSTALL_DIR)${NC}"

echo ""
echo -e "${GREEN}${BOLD}🎉 卸载完成！系统与 Antigravity 已恢复原貌，未残留任何冗余文件。${NC}"
echo ""
