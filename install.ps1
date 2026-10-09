# ==============================================================================
# Antigravity-ZH: Google Antigravity 官方级全界面简体中文套件 (Windows 原生安装器)
# GitHub: https://github.com/AIMarshallLee/antigravity-zh
# 支持在 Windows 10 / 11 PowerShell 中一键安装与全局注册
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   🚀 Antigravity-ZH 简体中文语言套件 (Windows 原生一键安装器)" -ForegroundColor Green
Write-Host "   致力于为 Antigravity 开发者提供极致的简体中文开发体验" -ForegroundColor White
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. 运行依赖体检 (Node.js & Python)
Write-Host "🔍 [1/5] 正在检查系统运行环境..." -ForegroundColor Cyan

$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Write-Host "❌ 未检测到 Node.js 运行环境！" -ForegroundColor Red
    Write-Host "👉 Antigravity 汉化守护引擎基于 Node.js 运行，请先安装 Node.js (推荐 v18+ 或 v20+)：" -ForegroundColor Yellow
    Write-Host "   可在终端运行: winget install OpenJS.NodeJS.LTS" -ForegroundColor White
    Write-Host "   或前往官网下载: https://nodejs.org/" -ForegroundColor White
    exit 1
} else {
    $nodeVer = & node -v
    Write-Host "  ✓ 检测到 Node.js: $nodeVer" -ForegroundColor Green
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Host "❌ 未检测到 Python 3 运行环境！" -ForegroundColor Red
    Write-Host "👉 请先安装 Python 3 (安装时请务必勾选 'Add Python to PATH')：" -ForegroundColor Yellow
    Write-Host "   可在终端运行: winget install Python.Python.3.11" -ForegroundColor White
    Write-Host "   或前往官网下载: https://www.python.org/downloads/" -ForegroundColor White
    exit 1
} else {
    $pyVer = & $pythonCmd.Source --version 2>&1
    Write-Host "  ✓ 检测到 Python: $pyVer" -ForegroundColor Green
}

# 2. 部署目标目录准备
$InstallDir = "$env:USERPROFILE\.antigravity-zh"
Write-Host ""
Write-Host "📦 [2/5] 正在部署核心汉化组件到: $InstallDir ..." -ForegroundColor Cyan

# 智能判断本地执行还是网络一键执行
$ScriptSourceDir = $PSScriptRoot
if ($ScriptSourceDir -and (Test-Path "$ScriptSourceDir\cli.py")) {
    Write-Host "  ✓ 检测到本地安装包，正在同步组件..." -ForegroundColor Green
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }
    Copy-Item -Path "$ScriptSourceDir\*" -Destination $InstallDir -Recurse -Force
} else {
    # 远程网络安装：智能选择最快镜像源
    Write-Host "  ⚡ 正在探测最佳下载通道 (GitHub 官方 vs 国内高速镜像)..." -ForegroundColor Yellow
    $GitUrl = "https://github.com/AIMarshallLee/antigravity-zh.git"
    
    # 快速探测网络连通性
    try {
        $testReq = Invoke-WebRequest -Uri "https://github.com" -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    } catch {
        $GitUrl = "https://ghproxy.net/https://github.com/AIMarshallLee/antigravity-zh.git"
        Write-Host "  ✓ 已自动启用国内高速代理通道: ghproxy.net" -ForegroundColor Green
    }

    if (Test-Path $InstallDir) {
        Write-Host "  ✓ 检测到已有安装，正在更新至最新版本..." -ForegroundColor Green
        try {
            git -C $InstallDir pull origin main 2>$null | Out-Null
        } catch {
            Remove-Item -Path $InstallDir -Recurse -Force -ErrorAction SilentlyContinue
            git clone --depth 1 $GitUrl $InstallDir
        }
    } else {
        git clone --depth 1 $GitUrl $InstallDir
    }
}

Write-Host "  ✓ 核心组件部署成功！" -ForegroundColor Green

# 3. 配置 Windows 用户环境变量 PATH
Write-Host ""
Write-Host "🔗 [3/5] 正在配置系统全局 CLI 快捷指令..." -ForegroundColor Cyan

$BinDir = "$InstallDir\bin"
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$BinDir*") {
    $NewUserPath = "$UserPath;$BinDir"
    [Environment]::SetEnvironmentVariable("Path", $NewUserPath, "User")
    $env:Path = "$env:Path;$BinDir"
    Write-Host "  ✓ 已成功将 $BinDir 写入用户 PATH 环境变量！" -ForegroundColor Green
} else {
    Write-Host "  ✓ PATH 环境变量已配置，无需重复添加。" -ForegroundColor Green
}

# 4. 注册 Windows 开机后台无黑框守护服务
Write-Host ""
Write-Host "🛡️ [4/5] 正在注册并启动后台自动守护服务 (Windows 静默常驻)..." -ForegroundColor Cyan

try {
    & $pythonCmd.Source "$InstallDir\cli.py" autostart enable | Out-Null
    Write-Host "  ✓ 守护服务已在后台静默启动！(开机自启、重启软件、切换标签均毫秒级自动保持汉化)" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️ 自动启动注册稍后可在终端通过 'antigravity-zh autostart enable' 手动重试。" -ForegroundColor Yellow
}

# 5. 立即触发一次热注入（如果客户端正在运行）
Write-Host ""
Write-Host "⚡ [5/5] 正在尝试为当前运行中的 Antigravity 注入汉化..." -ForegroundColor Cyan

try {
    & $pythonCmd.Source "$InstallDir\cli.py" ui | Out-Null
    Write-Host "  ✓ 热汉化指令已发送，当前窗口已刷新！" -ForegroundColor Green
} catch {
    Write-Host "  💡 当前 Antigravity 尚未启动，启动软件后守护进程将自动秒级完成汉化。" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "   🎉 恭喜！Antigravity-ZH 简体中文套件 (Windows) 已全部安装完成！" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "💡 日常使用小贴士：" -ForegroundColor White
Write-Host "   - 实时生效: 打开 Antigravity，界面将全自动保持简体中文。" -ForegroundColor Gray
Write-Host "   - 手动热刷: 在任何终端输入 antigravity-zh ui 即可重新注入。" -ForegroundColor Cyan
Write-Host "   - 运行体检: 在终端输入 antigravity-zh doctor 查看环境健康状态。" -ForegroundColor Cyan
Write-Host "   - 在线更新: 在终端输入 antigravity-zh update 同步最新词库。" -ForegroundColor Cyan
Write-Host "   - 技术社群: 欢迎加入飞书「昆仑增长 AI 交流群」（详见 GitHub 首页）" -ForegroundColor Magenta
Write-Host "   - 干净卸载: 随时在 PowerShell 中运行: powershell $InstallDir\uninstall.ps1" -ForegroundColor Gray
Write-Host ""
