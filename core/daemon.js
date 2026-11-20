#!/usr/bin/env node
/**
 * Antigravity 简体中文高频实时守护引擎 (Enhanced Daemon)
 * 实时监控所有 Antigravity 页面与会话，只要用户切换对话、刷新页面、开启新会话或重启软件，
 * 均在 1 秒内毫秒级自动补全汉化，彻底解决 SPA/React 路由切换导致的英文回滚问题。
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const SCRIPT_DIR = __dirname;
const INJECTOR_PATH = path.join(SCRIPT_DIR, 'injector.js');
let scriptContent = '';

try {
  scriptContent = fs.readFileSync(INJECTOR_PATH, 'utf-8');
} catch (e) {
  console.error('无法读取 injector.js:', e);
}

// 自动检测与修补 macOS App 启动 Wrapper，确保软件更新后始终带参数启动
function ensureWrapperInstalled() {
  if (process.platform === 'darwin') {
    const macosDir = '/Applications/Antigravity.app/Contents/MacOS';
    const mainBin = path.join(macosDir, 'Antigravity');
    const realBin = path.join(macosDir, 'Antigravity.bin');

    if (!fs.existsSync(mainBin)) return;

    try {
      const buffer = Buffer.alloc(4);
      const fd = fs.openSync(mainBin, 'r');
      fs.readSync(fd, buffer, 0, 4, 0);
      fs.closeSync(fd);

      if (!buffer.toString('utf-8').startsWith('#!')) {
        console.log(`[${new Date().toLocaleTimeString()}] 发现原生 Antigravity 二进制更新，正在自动修补自启动包装器...`);
        fs.copyFileSync(mainBin, realBin);
        fs.chmodSync(realBin, 0o755);

        const wrapperScript = `#!/bin/bash\nDIR="$(cd "$(dirname "$0")" && pwd)"\nexec "$DIR/Antigravity.bin" --remote-debugging-port=0 "$@"\n`;
        fs.writeFileSync(mainBin, wrapperScript, 'utf-8');
        fs.chmodSync(mainBin, 0o755);
        console.log(`[${new Date().toLocaleTimeString()}] ✅ 自启动包装器已成功自愈重置！`);
      }
    } catch (e) {
      // 容错忽略
    }
  }
}

function getDevToolsPort() {
  const possiblePaths = [];

  if (process.platform === 'win32') {
    const localAppData = process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local');
    const appData = process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming');
    const userProfile = process.env.USERPROFILE || os.homedir();

    possiblePaths.push(
      path.join(localAppData, 'Chromium', 'DevToolsActivePort'),
      path.join(localAppData, 'Chromium', 'User Data', 'DevToolsActivePort'),
      path.join(localAppData, 'Antigravity', 'DevToolsActivePort'),
      path.join(localAppData, 'Antigravity', 'User Data', 'DevToolsActivePort'),
      path.join(localAppData, 'antigravity', 'DevToolsActivePort'),
      path.join(appData, 'Chromium', 'DevToolsActivePort'),
      path.join(appData, 'Antigravity', 'DevToolsActivePort'),
      path.join(appData, 'antigravity', 'DevToolsActivePort'),
      path.join(userProfile, '.antigravity', 'DevToolsActivePort')
    );
  } else if (process.platform === 'darwin') {
    possiblePaths.push(
      path.join(os.homedir(), 'Library/Application Support/Chromium/DevToolsActivePort'),
      path.join(os.homedir(), 'Library/Application Support/Antigravity/DevToolsActivePort'),
      path.join(os.homedir(), 'Library/Application Support/antigravity/DevToolsActivePort')
    );
  } else {
    // Linux
    possiblePaths.push(
      path.join(os.homedir(), '.config/chromium/DevToolsActivePort'),
      path.join(os.homedir(), '.config/antigravity/DevToolsActivePort')
    );
  }

  for (const p of possiblePaths) {
    if (fs.existsSync(p)) {
      try {
        const content = fs.readFileSync(p, 'utf-8').trim().split('\n');
        const port = parseInt(content[0], 10);
        if (!isNaN(port) && port > 0) return port;
      } catch (e) {}
    }
  }
  return null;
}

// 针对单一页面的检查与注入
async function ensurePageInjected(page) {
  return new Promise((resolve) => {
    let ws;
    try {
      ws = new WebSocket(page.webSocketDebuggerUrl);
    } catch (e) {
      return resolve(false);
    }

    const timer = setTimeout(() => {
      try { ws.close(); } catch (e) {}
      resolve(false);
    }, 1500);

    ws.onopen = () => {
      // 1. 检查是否已被完整注入并正常运行
      ws.send(JSON.stringify({
        id: 101,
        method: "Runtime.evaluate",
        params: {
          expression: "!!(window.__ANTIGRAVITY_ZH_INJECTED__ && window.__ANTIGRAVITY_ZH_OBSERVER__ && window.__ANTIGRAVITY_ZH_INTERVAL__)",
          returnByValue: true
        }
      }));
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.id === 101) {
          const alreadyInjected = data.result?.result?.value;
          if (!alreadyInjected) {
            // 每次注入前确保读取磁盘上最新的 injector.js 脚本
            try { scriptContent = fs.readFileSync(INJECTOR_PATH, 'utf-8'); } catch (e) {}
            // 未注入，立即执行注入
            ws.send(JSON.stringify({
              id: 102,
              method: "Runtime.evaluate",
              params: {
                expression: scriptContent,
                returnByValue: true
              }
            }));
            // 同时注册页面导航保活
            ws.send(JSON.stringify({
              id: 103,
              method: "Page.addScriptToEvaluateOnNewDocument",
              params: { source: scriptContent }
            }));
          } else {
            clearTimeout(timer);
            ws.close();
            resolve(true);
          }
        } else if (data.id === 102) {
          clearTimeout(timer);
          ws.close();
          if (data.result?.exceptionDetails) {
            console.error(`[${new Date().toLocaleTimeString()}] ❌ 汉化注入脚本执行异常:`, data.result.exceptionDetails.text, data.result.exceptionDetails.exception?.description || '');
            resolve(false);
          } else {
            console.log(`[${new Date().toLocaleTimeString()}] ✅ 检测到新会话/页面未汉化，已自动完成中文补丁注入！(${page.title || 'Antigravity'})`);
            resolve(true);
          }
        }
      } catch (e) {
        clearTimeout(timer);
        try { ws.close(); } catch (err) {}
        resolve(false);
      }
    };

    ws.onerror = () => {
      clearTimeout(timer);
      resolve(false);
    };
  });
}

let isScanning = false;

async function scanAndProtect() {
  if (isScanning) return;
  isScanning = true;

  try {
    const port = getDevToolsPort();
    if (!port) return;

    const res = await fetch(`http://127.0.0.1:${port}/json`, { signal: AbortSignal.timeout(1000) });
    const targets = await res.json();
    const pages = targets.filter(t => t.type === 'page' && t.webSocketDebuggerUrl && !t.url.startsWith('data:text/html'));

    for (const page of pages) {
      await ensurePageInjected(page);
    }
  } catch (err) {
    // 允许静默失败，等待下一轮轮询
  } finally {
    isScanning = false;
  }
}

console.log('🛡️ Antigravity 增强版高频实时汉化守护已启动（1秒周期页面巡检 + 启动器自愈防护）...');
ensureWrapperInstalled();
setInterval(ensureWrapperInstalled, 15000);
scanAndProtect();
setInterval(scanAndProtect, 1000);
