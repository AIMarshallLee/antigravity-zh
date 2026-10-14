#!/usr/bin/env node
/**
 * Antigravity 简体中文高频实时守护引擎 (Enhanced Daemon)
 * 实时监控所有 Antigravity 页面与会话，只要用户切换对话、刷新页面、开启新会话或重启软件，
 * 均在 1 秒内毫秒级自动补全汉化，彻底解决 SPA/React 路由切换导致的英文回滚问题。
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 进程级防崩溃保护：网络断开、管道中断或调试接口关闭均不退出守护进程
process.on('uncaughtException', (err) => {
  // 忽略单次网络/WebSocket 异常，守护进程保持长效保活
});
process.on('unhandledRejection', (reason) => {
  // 忽略未处理的 Promise 拒绝
});

const SCRIPT_DIR = __dirname;
const INJECTOR_PATH = path.join(SCRIPT_DIR, 'injector.js');
let scriptContent = '';

try {
  scriptContent = fs.readFileSync(INJECTOR_PATH, 'utf-8');
} catch (e) {
  console.error('无法读取 injector.js:', e);
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
    let timer;

    const cleanup = () => {
      if (timer) {
        clearTimeout(timer);
        timer = null;
      }
      if (ws) {
        try { ws.close(); } catch (e) {}
      }
    };

    timer = setTimeout(() => {
      cleanup();
      resolve(false);
    }, 2000);

    try {
      ws = new WebSocket(page.webSocketDebuggerUrl);
    } catch (e) {
      cleanup();
      return resolve(false);
    }

    const safeSend = (msg) => {
      try {
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(msg));
          return true;
        }
      } catch (e) {}
      return false;
    };

    ws.onopen = () => {
      // 1. 检查是否已被注入
      safeSend({
        id: 101,
        method: "Runtime.evaluate",
        params: {
          expression: "!!window.__ANTIGRAVITY_ZH_INJECTED__",
          returnByValue: true
        }
      });
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
            safeSend({
              id: 102,
              method: "Runtime.evaluate",
              params: {
                expression: scriptContent,
                returnByValue: true
              }
            });
            // 同时注册页面导航保活
            safeSend({
              id: 103,
              method: "Page.addScriptToEvaluateOnNewDocument",
              params: { source: scriptContent }
            });
          } else {
            cleanup();
            resolve(true);
          }
        } else if (data.id === 102) {
          cleanup();
          if (data.result?.exceptionDetails) {
            console.error(`[${new Date().toLocaleTimeString()}] ❌ 汉化注入脚本执行异常:`, data.result.exceptionDetails.text, data.result.exceptionDetails.exception?.description || '');
            resolve(false);
          } else {
            console.log(`[${new Date().toLocaleTimeString()}] ✅ 检测到新会话/页面未汉化，已自动完成中文补丁注入！(${page.title || 'Antigravity'})`);
            resolve(true);
          }
        }
      } catch (e) {
        cleanup();
        resolve(false);
      }
    };

    ws.onerror = () => {
      cleanup();
      resolve(false);
    };

    ws.onclose = () => {
      cleanup();
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
    const pages = targets.filter(t => t.type === 'page' && t.webSocketDebuggerUrl);

    for (const page of pages) {
      await ensurePageInjected(page);
    }
  } catch (err) {
    // 允许静默失败，等待下一轮轮询
  } finally {
    isScanning = false;
  }
}

console.log('🛡️ Antigravity 增强版高频实时汉化守护已启动（1秒周期页面巡检）...');
scanAndProtect();
setInterval(scanAndProtect, 1000);
