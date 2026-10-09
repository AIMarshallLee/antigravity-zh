# ==============================================================================
# Antigravity-ZH: Google Antigravity 简体中文套件 (Windows 原生卸载器)
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$InstallDir = "$env:USERPROFILE\.antigravity-zh"

Write-Host "🗑️ 正在干净卸载 Antigravity-ZH 简体中文套件..." -ForegroundColor Yellow

# 1. 停止并移除后台守护服务
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) { $pythonCmd = Get-Command py -ErrorAction SilentlyContinue }

if ($pythonCmd -and (Test-Path "$InstallDir\cli.py")) {
    try {
        & $pythonCmd.Source "$InstallDir\cli.py" autostart disable | Out-Null
    } catch {}
}

# 双重保障：清理 Startup 目录中的启动脚本
$appdata = os.environ.get("APPDATA")
$StartupVbs = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\AntigravityZH-Daemon.vbs"
if (Test-Path $StartupVbs) {
    Remove-Item $StartupVbs -Force -ErrorAction SilentlyContinue
}

# 杀死运行中的守护进程
try {
    Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*daemon.js*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
} catch {}

# 2. 从 PATH 中移除
$BinDir = "$InstallDir\bin"
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -like "*$BinDir*") {
    $NewUserPath = ($UserPath.Split(';') | Where-Object { $_ -ne $BinDir -and $_ -ne "" }) -join ';'
    [Environment]::SetEnvironmentVariable("Path", $NewUserPath, "User")
}

# 3. 删除安装目录
if (Test-Path $InstallDir) {
    Remove-Item -Path $InstallDir -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "✅ Antigravity-ZH 及其后台守护服务已从 Windows 完全干净卸载！" -ForegroundColor Green
Write-Host "💡 重启 Antigravity 即可恢复原生英文界面。" -ForegroundColor White
