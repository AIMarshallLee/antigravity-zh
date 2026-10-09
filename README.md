# 🚀 Antigravity-ZH | 谷歌 Antigravity 全链路高精汉化开发套件

> 为 Google Antigravity 打造的零破坏、纯净热注入、全自动保持的极致简体中文开发套件。

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: macOS](https://img.shields.io/badge/Platform-macOS-brightgreen.svg)]()
[![Node: >=18](https://img.shields.io/badge/Node-%3E%3D18-blue.svg)](https://nodejs.org/)
[![Python: >=3.9](https://img.shields.io/badge/Python-%3E%3D3.9-yellow.svg)](https://python.org/)
[![Status: Active](https://img.shields.io/badge/Status-Maintained-success.svg)]()

**[一键安装](#-极速一键安装)** • **[核心特性](#-核心特性)** • **[运行架构](#-工作原理与架构)** • **[CLI 指令](#%EF%B8%8F-cli-常用命令)** • **[常见问题](#-常见问题-faq)**

</div>

---

## 💡 为什么需要 Antigravity-ZH？

Google Antigravity 是一款强大的 AI 原生 IDE / 智能体客户端，但目前原生未提供完整的简体中文界面包：
- **修改 locale 往往无效**：客户端主界面是由 Electron + Chromium 驱动的高性能 SPA 单页应用，修改 VS Code 的 `argv.json` 无法作用于主界面与外层设置。
- **生硬机翻破坏代码生态**：粗暴的汉化脚本容易误将开发者自己的工程项目（如 `Agent`、`AIcode`）或底层技术协议（`MCP`、`Codex`、`Google Chrome`）强行翻译，造成严重视觉困扰。
- **版本更新汉化失效**：每次 Antigravity 后台更新或重启，传统汉化通常会被覆盖。

**Antigravity-ZH 套件彻底解决了以上所有痛点！**

---

## ✨ 核心特性

- 🌐 **100% 深度高精汉化**：
  - 侧边栏所有操作、历史会话分组筛选（`Group By`、`Sort Conversations`）与多级菜单。
  - 常规设置、应用程序、外观主题、大模型管理、危险区域等全部二级设置面板。
  - 大模型用量配额面板及动态实时重置倒计时（例如：`3 小时 15 分钟 后重置`）。
  - 全量快捷键指南面板（包含导航、会话、布局控制全部按键说明）。
  - 右上角更多菜单（重命名、置顶、归档、多向分屏、信息复制等全部级联项）。
- 🛡️ **专有名词与工程原生保护**：
  - 严格识别并保留用户的真实工程目录与代码库名称。
  - `MCP`、`Codex`、`Webcodex`、`Cockpit`、`Mac`、`Google Chrome`、`Gemini`、`Claude`、`GPT` 等专有名词 100% 保持原生英文规范。
- 🔄 **毫秒级更新自愈 (Auto-Healing Daemon)**：
  - 基于 macOS 原生 `LaunchAgent` 系统守护机制，自动侦听 Antigravity 客户端生命周期。
  - 无论系统重启、应用升级新版本还是新开对话标签，**3 秒内全自动保活汉化，无需用户任何手动干预**！
- 🔒 **零破坏原生安全架构**：
  - 不篡改、不解包 Electron 二进制或 `app.asar`，不破坏应用官方代码签名。
  - 通过 Chrome DevTools Protocol (CDP) WebSocket 接口在内存中热载入，安全合规，绝无安全隐患。
- 🧠 **TreeWalker 穿透式 DOM 渲染引擎**：
  - 针对被 `<kbd>`、`<a>` 标签切碎的内联文本碎片，提供深层节点遍历重组，彻底杜绝文字排版错位与漏翻。

---

## ⚡ 极速一键安装

打开 macOS 终端，直接粘贴执行以下命令：

```bash
# 官方标准一键安装 (推荐)
curl -fsSL https://raw.githubusercontent.com/AIMarshallLee/antigravity-zh/main/install.sh | bash

# 国内高速镜像一键安装 (若遇到网络超时请用此命令)
curl -fsSL https://ghproxy.net/https://raw.githubusercontent.com/AIMarshallLee/antigravity-zh/main/install.sh | bash
```

> **提示**：安装脚本会自动完成程序部署、环境依赖体检、全局 CLI 命令注册与 LaunchAgent 开机守护配置。

---

## 🛠️ CLI 常用命令

安装完成后，你可以在系统的任何终端随时调用 `antigravity-zh` 工具：

| 命令 | 说明 |
| :--- | :--- |
| `antigravity-zh ui` | **立即刷新汉化**：向当前正在运行的 Antigravity 窗口热载入最新汉化 |
| `antigravity-zh update` | **在线更新**：一键从 GitHub 拉取最新的汉化词典与补丁并立即生效 |
| `antigravity-zh doctor` | **系统体检**：检测 IDE 语言环境、Git 中文转义支持与守护进程运行状态 |
| `antigravity-zh autostart status` | **查看状态**：查看开机自启与后台自动保活守护进程的实时运行状态 |
| `antigravity-zh autostart enable` | **开启守护**：启用开机自启与版本更新自动保活服务 |
| `antigravity-zh autostart disable`| **关闭守护**：停止后台保活守护服务 |
| `antigravity-zh enable` | **最佳实践**：一键应用 Git 中文文件名防乱码等开发环境推荐配置 |

---

## 🏗️ 工作原理与架构

```
┌────────────────────────────────────────────────────────┐
│                   macOS 用户环境                       │
└────────────────────────────────────────────────────────┘
                           │
       ┌───────────────────┴───────────────────┐
       ▼                                       ▼
【macOS LaunchAgent】                 【antigravity-zh CLI】
 (系统级开机守护服务)                  (终端控制台快捷入口)
       │                                       │
       │ (1秒周期监听 CDP 端口)                │
       ▼                                       ▼
┌────────────────────────────────────────────────────────┐
│   Chrome DevTools Protocol (CDP) WebSocket 内存热注入   │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│              Google Antigravity 桌面客户端             │
│  - MutationObserver 动态节点侦听                       │
│  - TreeWalker 深度 DOM 穿透引擎                        │
│  - 项目名白名单与专有名词隔离保护网                    │
└────────────────────────────────────────────────────────┘
```

---

## ❓ 常见问题 (FAQ)

### 1. 软件更新后，汉化会丢失吗？
**不会。** Antigravity-ZH 随附系统级 `LaunchAgent` 守护服务，会在后台自动监测 Antigravity 的运行。一旦检测到新版本启动或新页面生成，将在 1~3 秒内全自动注入汉化补丁，彻底实现“无感使用”。

### 2. 这个工具会修改我的 Antigravity 原始安装文件吗？
**绝不修改。** 本项目采用无侵入的 CDP（Chrome 调试协议）热注入方式，只在运行时向渲染进程注入界面汉化逻辑，完全不改动 `/Applications/Antigravity.app` 包内的任何二进制文件与 `app.asar`。

### 3. 如何彻底卸载？
如果你想恢复纯英文原生环境，在终端运行一行命令即可彻底干净卸载：

```bash
curl -fsSL https://raw.githubusercontent.com/AIMarshallLee/antigravity-zh/main/uninstall.sh | bash
```

---

## 🤝 贡献与反馈

欢迎提交 PR 或 Issue 一起完善汉化词典！
- 发现界面有漏翻或翻译不准确的地方？欢迎提交 [Issue](https://github.com/AIMarshallLee/antigravity-zh/issues)。
- 欢迎 Fork 本项目并贡献更多专属特性！

## 💬 交流与社群

欢迎加入 **Antigravity 开发者技术交流群**，与全国第一批 Antigravity 极客交流 Agent 工作流、汉化技巧与开发心得！

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="assets/feishu-group.jpg" width="220" alt="飞书交流群" /><br />
        <b>飞书交流群 (永久有效)</b>
      </td>
      <td align="center">
        <img src="assets/wechat-group.png" width="220" alt="微信交流群" /><br />
        <b>微信技术交流群</b>
      </td>
    </tr>
  </table>
  <p><i>扫码即可加入交流社群（若二维码过期可在 Issue 中留言获取最新加入方式）</i></p>
</div>

---

## 📄 开源许可证

本项目基于 [MIT License](LICENSE) 协议完全开源。

