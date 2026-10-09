#!/usr/bin/env node
/**
 * Antigravity 界面汉化补丁注入程序
 * 通过 Chrome DevTools Protocol (CDP) WebSocket 接口实时注入汉化脚本
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

async function getDevToolsPort() {
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

async function injectChinese() {
  const port = await getDevToolsPort();
  if (!port) {
    console.error('❌ 未找到 Antigravity 运行时的 DevToolsActivePort，请确认 Antigravity 已启动。');
    process.exit(1);
  }

  const endpoint = `http://127.0.0.1:${port}/json`;
  let pages = [];
  try {
    const res = await fetch(endpoint);
    pages = await res.json();
  } catch (err) {
    console.error(`❌ 连接 Antigravity 调试接口失败 (127.0.0.1:${port}):`, err.message);
    process.exit(1);
  }

  const page = pages.find(p => p.type === 'page' && p.webSocketDebuggerUrl);
  if (!page) {
    console.error('❌ 未在当前 Antigravity 进程中找到可交互的活动页面。');
    process.exit(1);
  }

  const scriptPath = path.join(__dirname, 'injector.js');
  const scriptContent = fs.readFileSync(scriptPath, 'utf-8');

  return new Promise((resolve, reject) => {
    const ws = new WebSocket(page.webSocketDebuggerUrl);

    ws.onopen = () => {
      // 1. 立即在当前页面执行汉化脚本
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: {
          expression: scriptContent,
          returnByValue: true
        }
      }));

      // 2. 注册为持久化注入（页面刷新或重新导航时自动生效）
      ws.send(JSON.stringify({
        id: 2,
        method: 'Page.addScriptToEvaluateOnNewDocument',
        params: {
          source: scriptContent
        }
      }));
    };

    let doneCount = 0;
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.id === 1) {
        if (data.error) {
          console.error('⚠️ 执行汉化脚本报错:', data.error);
        } else {
          console.log('✅ 当前界面汉化已即刻生效！');
        }
        doneCount++;
      }
      if (data.id === 2) {
        console.log('✅ 页面持久化汉化监听器已注册 (刷新或切换标签保持中文)！');
        doneCount++;
      }
      if (doneCount >= 2) {
        ws.close();
        resolve(true);
      }
    };

    ws.onerror = (err) => {
      console.error('❌ WebSocket 连接出错:', err);
      reject(err);
    };

    setTimeout(() => {
      ws.close();
      resolve(true);
    }, 4000);
  });
}

injectChinese().catch(err => {
  console.error('注入执行异常:', err);
  process.exit(1);
});
