#!/usr/bin/env bash
# ==============================================================================
#  Antigravity-ZH 一键极速安装脚本 (macOS)
#  项目地址: https://github.com/AIMarshallLee/antigravity-zh
# ==============================================================================

set -e

# 颜色与样式
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${CYAN}${BOLD}"
echo "=================================================================="
echo "   🚀 欢迎安装 Antigravity-ZH (全链路纯净高精汉化套件)            "
echo "   专为 Google Antigravity 开发者打造的零破坏实时汉化工具         "
echo "=================================================================="
echo -e "${NC}"

# 1. 检查运行系统
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ 抱歉，本套件目前专为 macOS 系统深度定制。暂不支持 Linux / Windows。${NC}"
    exit 1
fi

# 2. 检查依赖
echo -e "${BLUE}🔍 [1/5] 正在检查本地基础依赖环境...${NC}"

if ! command -v node >/dev/null 2>&1; then
    echo -e "${RED}❌ 未检测到 Node.js，请先安装 Node.js (推荐 v20+): https://nodejs.org/${NC}"
    exit 1
fi

NODE_MAJOR=$(node -v | cut -d'.' -f1 | sed 's/v//')
if [ "$NODE_MAJOR" -lt 18 ]; then
    echo -e "${YELLOW}⚠️ 警告: 检测到当前 Node.js 版本较低 ($(node -v))，建议使用 v18 或更高版本。${NC}"
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}❌ 未检测到 Python 3，请先安装 Python 3。${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ 基础运行环境完备 (Node.js $(node -v), Python $(python3 --version | cut -d' ' -f2))${NC}"

# 3. 确定安装路径
INSTALL_DIR="$HOME/.antigravity-zh"
SCRIPT_SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"

echo -e "${BLUE}📦 [2/5] 正在部署核心程序文件到: ${INSTALL_DIR} ...${NC}"

if [ -f "${SCRIPT_SOURCE_DIR}/cli.py" ] && [ -d "${SCRIPT_SOURCE_DIR}/core" ]; then
    # 本地目录执行安装
    mkdir -p "${INSTALL_DIR}"
    cp -R "${SCRIPT_SOURCE_DIR}/"* "${INSTALL_DIR}/"
else
    # 远程 curl 管道执行安装
    if [ -d "${INSTALL_DIR}" ]; then
        rm -rf "${INSTALL_DIR}"
    fi
    git clone --depth 1 https://github.com/AIMarshallLee/antigravity-zh.git "${INSTALL_DIR}"
fi

chmod +x "${INSTALL_DIR}/bin/antigravity-zh"
chmod +x "${INSTALL_DIR}/cli.py"
chmod +x "${INSTALL_DIR}/core/inject.js"
chmod +x "${INSTALL_DIR}/core/daemon.js"
echo -e "${GREEN}  ✓ 核心组件部署成功${NC}"

# 4. 创建系统全局软链接
echo -e "${BLUE}🔗 [3/5] 正在配置系统全局 CLI 快捷指令...${NC}"

TARGET_BIN_DIR="/usr/local/bin"
USER_BIN_DIR="$HOME/.local/bin"
LINKED=false

if [ -w "$TARGET_BIN_DIR" ]; then
    ln -sf "${INSTALL_DIR}/bin/antigravity-zh" "$TARGET_BIN_DIR/antigravity-zh"
    echo -e "${GREEN}  ✓ 已软链接全局命令至: ${TARGET_BIN_DIR}/antigravity-zh${NC}"
    LINKED=true
else
    mkdir -p "$USER_BIN_DIR"
    ln -sf "${INSTALL_DIR}/bin/antigravity-zh" "$USER_BIN_DIR/antigravity-zh"
    echo -e "${GREEN}  ✓ 已软链接全局命令至: ${USER_BIN_DIR}/antigravity-zh${NC}"
    LINKED=true
    
    # 检查 PATH 是否包含 ~/.local/bin
    if [[ ":$PATH:" != *":$USER_BIN_DIR:"* ]]; then
        SHELL_RC="$HOME/.zshrc"
        if [ "$SHELL" = "/bin/bash" ]; then
            SHELL_RC="$HOME/.bash_profile"
        fi
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
        echo -e "${YELLOW}  👉 已将 ~/.local/bin 写入 ${SHELL_RC}。当前终端可运行 'source ${SHELL_RC}' 生效。${NC}"
    fi
fi

# 5. 注册开机自启与版本更新自动保活守护服务
echo -e "${BLUE}🛡️ [4/5] 正在注册并启动后台自动守护进程 (LaunchAgent)...${NC}"
python3 "${INSTALL_DIR}/cli.py" autostart enable >/dev/null 2>&1 || true
echo -e "${GREEN}  ✓ 守护进程已启动，版本更新、重启电脑、新开会话均自动保持汉化！${NC}"

# 6. 立即触发一次热注入（如果客户端正在运行）
echo -e "${BLUE}⚡ [5/5] 正在尝试为当前运行中的 Antigravity 注入汉化...${NC}"
python3 "${INSTALL_DIR}/cli.py" ui >/dev/null 2>&1 || true

echo ""
echo -e "${GREEN}${BOLD}=================================================================="
echo "   🎉 恭喜！Antigravity-ZH 简体中文套件已全部安装完成！           "
echo "=================================================================="
echo -e "${NC}"
echo -e "💡 ${BOLD}日常使用小贴士：${NC}"
echo -e "   - 实时生效: 打开或切换 Antigravity，界面将全自动保持简体中文。"
echo -e "   - 手动热刷: 终端随时输入 ${CYAN}antigravity-zh ui${NC} 即可重新注入。"
echo -e "   - 运行体检: 终端输入 ${CYAN}antigravity-zh doctor${NC} 查看环境健康状态。"
echo -e "   - 卸载清理: 随时运行 ${CYAN}curl -fsSL ... | bash${NC} 或执行 ${CYAN}~/.antigravity-zh/uninstall.sh${NC}。"
echo ""
