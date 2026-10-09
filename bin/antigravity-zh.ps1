# Antigravity-ZH PowerShell Launcher
$ScriptDir = Split-Path -Parent $PSScriptRoot

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command py -ErrorAction SilentlyContinue
}

if ($pythonCmd) {
    & $pythonCmd.Source "$ScriptDir\cli.py" @args
} else {
    Write-Error "[Antigravity-ZH Error] 未找到 Python 3，请确认 Python 已安装并添加到 PATH！"
    exit 1
}
