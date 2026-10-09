/**
 * Antigravity 终极全量高精汉化引擎 (全界面 100% 深度汉化版)
 * 覆盖：
 * 1. 危险区域 (Danger Zone / Delete Project / 动态包含活跃对话 / 删除项目按钮)
 * 2. 快捷键指南 (分类 RECOMMENDED / NAVIGATION / CONVERSATION / LAYOUT 及所有操作项)
 * 3. 自定义扩展与 Token 消耗细分 (Token Usage / Show X breakdowns / 说明文案)
 * 4. 远程控制与应用设置 (Scan the code to open... / copy link / 客户端版本等)
 * 5. 编辑器、反馈与下拉菜单 (Modified in X projects / Learn more / Feedback)
 * 6. 严密保护用户项目名 (AIcode, Agent 等) 与 MCP 专有名词
 */
(() => {
  if (window.__ANTIGRAVITY_ZH_INTERVAL__) {
    clearInterval(window.__ANTIGRAVITY_ZH_INTERVAL__);
    window.__ANTIGRAVITY_ZH_INTERVAL__ = null;
  }
  if (window.__ANTIGRAVITY_ZH_OBSERVER__) {
    try { window.__ANTIGRAVITY_ZH_OBSERVER__.disconnect(); } catch (e) {}
    window.__ANTIGRAVITY_ZH_OBSERVER__ = null;
  }
  window.__ANTIGRAVITY_ZH_INJECTED__ = true;

  // 用户项目/文件夹保护白名单 (严禁汉化)
  const USER_PROJECT_NAMES = new Set([
    "Agent", "agent", "AIcode", "AIcode/", "opc-event-radar", "ai-tools-navigator-main",
    "host-c-kadadesk", "GhostDesk", "Kunlun-AI-Opportunity-Audit",
    "OMNI-ContentForge", "Kadadesk", "Hermes-agent", "WorkBuddy运营"
  ]);

  // 全量静态字典 (按词条精准匹配)
  const STATIC_DICT = {
    // 侧边栏与主窗口
    "New Conversation": "新建对话",
    "Conversation History": "历史对话",
    "Automations": "自动化任务",
    "Customizations": "自定义扩展",
    "Pinned Conversations": "置顶对话",
    "Projects": "项目列表",
    "Settings": "系统设置",
    "Rules": "全局规则",
    "Skills": "技能库",
    "MCP Servers": "MCP 服务",
    "Plugins": "插件中心",
    "Workspaces": "工作空间",
    "Artifacts": "生成产物",
    "Terminal": "终端控制台",
    "Agent Status": "智能体状态",
    "See less": "收起",
    "See more": "展开更多",
    "Load older messages": "加载历史消息",
    "Conversation Log": "对话运行日志",
    "Ran commands": "已执行命令",
    "Working": "处理中",
    "Thinking": "深度思考中",
    "Done": "已完成",
    "Recent": "最近记录",
    "All Conversations": "全部对话",
    "Search conversations": "搜索对话历史...",
    "Search projects": "搜索项目...",
    "Restart to Update": "重启以更新",
    "Restart to Update ->": "重启以更新 ->",

    // 项目选择器 (Project Picker)
    "No Project": "无项目",
    "New Project": "新建项目",
    "Quick Start": "快速开始",
    "Open Project": "打开项目",
    "Manage Projects": "管理项目",
    "Recent Projects": "最近项目",

    // 侧边栏会话筛选与排序菜单 (Group By / Sort Conversations)
    "Group By": "分组依据",
    "Workspace": "工作空间",
    "Status": "状态",
    "None": "不分组",
    "Sort Conversations": "会话排序",
    "Last Updated": "最近更新时间",
    "Last Prompt": "最新输入时间",
    "Alphabetical (A-Z)": "按字母排序 (A-Z)",
    "Date Added": "创建添加时间",
    "View": "视图",
    "Archived Only": "仅看已归档",
    "Filter": "筛选",
    "Display": "显示项",
    "Subtitles": "副标题",
    "Worktree": "工作树",
    "Last 7 days": "最近 7 天",
    "Last 30 days": "最近 30 天",
    "Today": "今天",
    "Yesterday": "昨天",
    "All": "全部",
    "Active": "活跃",
    "Archived": "已归档",

    // 自动化任务面板 (Automations)
    "Create with Prompt": "通过提示词创建",
    "+ New": "+ 新建",
    "Search automations...": "搜索自动化任务...",
    "No automations configured.": "尚未配置任何自动化任务。",

    // 会话右上角更多操作菜单 (More Options & Split/Copy)
    "Rename": "重命名",
    "Pin": "置顶对话",
    "Unpin": "取消置顶",
    "Archive": "归档会话",
    "Unarchive": "取消归档",
    "Split": "分屏",
    "Split Right": "向右分屏",
    "Split Down": "向下分屏",
    "Split Left": "向左分屏",
    "Split Up": "向上分屏",
    "Replace With New": "替换为新对话",
    "Conversation Name": "会话名称",
    "Conversation ID": "会话 ID",
    "Project Name": "项目名称",
    "Branch Name": "分支名称",

    // 侧边栏会话简要说明/标题汉化 (专有名词严格保留)
    "Install And Open Antigravity Tools": "安装并打开 Antigravity 工具",
    "Codex Adaptive Agents Installation": "Codex 自适应智能体安装",
    "Install Webcodex Tool": "安装 Webcodex 工具",
    "Install Cockpit Tools": "安装 Cockpit 工具",
    "Codex Integration Inquiry": "Codex 集成方案咨询",
    "Optimizing Disk Storage Space": "优化磁盘存储空间",
    "Troubleshooting Mac Software Installation": "Mac 软件安装故障排查",
    "SEO Velocity Project Status": "SEO Velocity 项目状态",
    "Building Logic Notes App": "构建 Logic Notes 应用",
    "Openclaw Installation Check": "Openclaw 安装检查",
    "Install ScrapeGraphAI": "安装 ScrapeGraphAI",

    // 设置左侧二级导航项
    "Application": "应用程序",
    "Appearance": "外观与主题",
    "Models": "大模型管理",
    "Show All": "显示全部",
    "Not in Project": "未归属项目",
    "Conversations": "历史会话",
    "Shortcuts": "快捷键指南",
    "Provide Feedback": "提交反馈",
    "General": "常规设置",
    "Keybindings": "快捷键设定",
    "Permissions": "安全权限",
    "Experimental": "实验性特性",
    "About": "关于 Antigravity",
    "Check for Updates": "检查版本更新",
    "Custom Instructions": "自定义指令",
    "User Preferences": "用户偏好",
    "Account": "账户与套餐",
    "Developer": "开发者工具",

    // 危险区域 (Danger Zone)
    "Danger Zone": "危险区域",
    "Delete Project": "删除项目",
    "Permanently delete": "永久删除",
    "including": "，包含",
    "active conversations": "个活跃对话",
    "active conversations.": "个活跃对话。",
    "Project": "项目",
    "删除Project": "删除项目",

    // 下拉菜单与链接碎片
    "Modified in": "已自定义于",
    "projects": "个项目",
    "Learn more": "了解详情",
    "Learn more.": "了解详情",

    // 工具权限与行为规范
    "Tool Permissions": "工具权限设置",
    "Modify permissions for file, terminal, and MCP tools.": "修改代码文件、终端命令及 MCP 工具的访问权限。",
    "Type": "输入",
    "and select": "并选择",
    "to have the agent generate a plan.": "让智能体生成执行方案。",
    "Type / and select plan to have the agent generate a plan.": "输入 / 并选择 plan 让智能体生成执行方案。",
    "Configure the browser subagent. It requires": "配置浏览器子智能体。此功能需要已安装",
    "to be installed.": "。",
    "Configure the browser subagent. It requires Google Chrome to be installed.": "配置浏览器子智能体。此功能需要已安装 Google Chrome。",
    "The browser subagent can be invoked by typing /browser in the conversation input box.": "在对话输入框输入 /browser 即可调用浏览器智能体。",

    // 自定义扩展与 Token 消耗细分
    "Token Usage": "Token 消耗统计",
    "Other Customizations": "其他自定义项",
    "The breakdown below shows token usage from customizations like rules, skills, and MCP. If a budget is exceeded, large rules are demoted to path pointers and large customizations are excluded automatically.": "下方细分展示了规则、技能与 MCP 等自定义项的 Token 消耗。若超出预算配额，大型规则将降级为路径指针，大型自定义项将自动排除。",
    "Build With Google Plugins": "Build With Google 官方插件",
    "Browse and enable plugins from the Build With Google catalog.": "浏览并启用 Build With Google 目录中的官方扩展插件。",
    "Customize": "自定义配置",
    "Configure default behaviors, skills, and MCP servers.": "配置默认智能体行为、技能库及 MCP 服务。",

    // 快捷键指南面板 (Keyboard Shortcuts)
    "Keyboard shortcuts for quick navigation and control.": "用于快速导航与控制的操作快捷键指南。",
    "RECOMMENDED": "推荐常用",
    "Recommended": "推荐常用",
    "NAVIGATION": "界面导航",
    "Navigation": "界面导航",
    "CONVERSATION": "会话操作",
    "Conversation": "会话操作",
    "LAYOUT CONTROLS": "布局控制",
    "Layout Controls": "布局控制",
    "Open Conversation Picker": "打开会话选择器",
    "Open File Search": "打开文件搜索",
    "Focus Input": "聚焦输入框",
    "New Conversation": "新建对话",
    "File Picker": "文件选择器",
    "Automations": "自动化任务",
    "Select Previous Conversation": "切换到上一个会话",
    "Select Next Conversation": "切换到下一个会话",
    "Previous Pane Tab": "上一个面板标签页",
    "Next Pane Tab": "下一个面板标签页",
    "Open Settings": "打开系统设置",
    "Toggle Model Selector": "切换大模型选择器",
    "Toggle Voice Recording": "切换语音录制",
    "Find in Pane": "在当前窗格中查找",
    "Add to Chat/Quote": "添加到对话 / 引用",
    "Toggle Sidebar": "切换侧边栏展开/折叠",
    "Toggle Auxiliary Pane": "切换辅助窗格展开/折叠",
    "Toggle Terminal": "切换终端控制台",

    // 远程控制与应用设置
    "Scan the code to open this device in Remote Control, or": "扫描二维码以在远程控制中打开此设备，或",
    "copy link": "复制链接",
    "copy link.": "复制链接",
    "Prevent Sleep": "防止系统休眠",
    "Prevent the computer from sleeping while the app is running.": "在应用运行期间防止电脑自动进入睡眠状态。",
    "Keep In Menu Bar": "常驻顶部菜单栏",
    "Keep the app accessible from the menu bar and running in the background when all windows are closed.": "当所有窗口关闭时，保持应用在后台运行并可从顶部菜单栏随时唤起。",
    "Remote Control": "远程控制",
    "Enable Remote Control": "开启远程控制功能",
    "Work with local agents from another device.": "支持从其他终端设备无缝协同本地智能体。",
    "Device Name": "设备名称",
    "Notifications": "系统通知",
    "Notification Settings": "通知权限设置",
    "To modify notification settings, open your operating system's system preferences.": "若要调整通知偏好，请在操作系统的系统设置中进行更改。",
    "Open System Preferences": "打开系统设置",
    "Version": "版本信息",
    "App version": "客户端版本",
    "Advanced Settings": "高级进阶设置",

    // 编辑器设置
    "Editor Settings": "编辑器设置",
    "Configure editor-specific behaviors and shortcuts.": "配置编辑器专用行为与快捷键。",
    "Marketplace": "扩展插件市场",
    "Marketplace Item URL": "插件市场项目 URL",
    "Changes the base URL on each extension page. You must restart Antigravity to use the new marketplace after changing this value.": "更改每个插件页面的基础 URL。更改此值后必须重启 Antigravity 才能使用新的市场。",
    "Marketplace Gallery URL": "插件市场目录 URL",
    "Changes the base URL for marketplace search results. You must restart Antigravity to use the new marketplace after changing this value.": "更改插件市场搜索结果的基础 URL。更改此值后必须重启 Antigravity 才能生效。",
    "Selection Actions": "选中文本操作",
    "Show Selection Actions": "显示选中文本操作栏",
    "Show \"Edit\" and \"Chat\" buttons when selecting text in the editor.": "在编辑器中选中文本时显示“编辑”和“对话”快捷按钮。",
    "To modify editor settings, open Settings within the editor window.": "若要修改编辑器详细设置，请在编辑器窗口中打开设置。",
    "Open Editor Settings": "打开编辑器设置",

    // 反馈面板
    "Feedback Type": "反馈类型",
    "Bug Report": "问题报告 (Bug)",
    "Feature Request": "功能建议",
    "Auth and Billing": "认证与计费",
    "Remote Control Issue": "远程控制问题",
    "General Feedback": "一般反馈",
    "Description": "问题描述",
    "Please describe the issue in detail. The more actionable your feedback, the quicker our team can address your request. Some helpful information includes:": "请详细描述问题。反馈越具体，我们的团队就能越快处理你的请求。有帮助的信息包括：",
    "Steps to reproduce the issue": "复现步骤",
    "Expected behavior": "预期行为",
    "Actual behavior": "实际行为",
    "Any error messages": "任何错误信息",
    "Any relevant information": "任何相关信息",
    "Steps to Reproduce": "复现步骤",
    "Attach a screenshot (optional)": "附带屏幕截图 (可选)",
    "Attach Antigravity server logs": "附带 Antigravity 服务端日志",
    "Visit": "访问",
    "Legal Help": "法律帮助",
    "to ask for content changes for legal reasons.": "以因法律原因申请内容变更。",

    // Models & Usage 大模型管理界面
    "Models & Usage": "大模型与使用配额",
    "Manage your model quota and credits.": "管理你的大模型配额与抵扣额度。",
    "Plan": "订阅方案",
    "Model Credits": "AI 抵扣额度",
    "Enable AI Credit Overages": "启用 AI 抵扣额度超额抵扣",
    "When toggled on, Antigravity will use your AI credits to fulfill model requests once you're out of model quota. Antigravity will always use your model quota first before using AI credits.": "开启后，当模型配额耗尽时，Antigravity 将使用你的 AI 额度来处理请求。Antigravity 将始终优先消耗模型配额，然后再使用 AI 额度。",
    "Gemini Models": "Gemini 系列模型",
    "Claude and GPT models": "Claude 与 GPT 系列模型",
    "Weekly Limit Remaining": "本周剩余可用额度",
    "Five Hour Limit Remaining": "5 小时剩余可用额度",
    "Model Quota": "大模型配额",
    "Refresh quota and credits data": "刷新配额与额度数据",

    // 常规与项目设置面板
    "Configure agent execution, queued message delivery, and permissions.": "配置智能体执行行为、消息排队策略及权限规则。",
    "Manage project folders, agent settings, and permissions.": "管理项目文件夹、智能体设定及权限规则。",
    "Manage your plan, credentials, and general preferences.": "管理你的订阅方案、凭据及常规偏好设置。",
    "Execution": "执行策略",
    "Queued Messages": "排队消息机制",
    "Configure when follow-up messages are sent.": "配置后续跟进消息的发送时机。",
    "Keyboard shortcuts": "键盘快捷键",
    "Queue": "排队等待",
    "Send Immediately": "立即发送",

    "Global Permissions": "全局权限管理",
    "Permission Settings": "权限设置",
    "Configure global allowed and denied resource permissions.": "配置全局允许与拒绝访问的资源权限。",
    "Configure global allowed and denied resource permissions. Learn more.": "配置全局允许与拒绝访问的资源权限。了解详情。",
    "Also includes Global Permissions when working in this project. Learn more.": "在本项目中工作时同时包含全局权限。了解详情。",
    "Also includes": "在本项目中工作时，亦包含",
    "when working in this project.": "（在本项目中生效）。",
    "when working in this project": "（在本项目中生效）",
    "Agent settings and permissions for conversations outside of projects.": "配置未归属项目的会话智能体设定及权限规则。",
    "Agent settings and permissions for conversations outside of projects": "配置未归属项目的会话智能体设定及权限规则。",
    "Permission Preset": "权限预设方案",
    "Controls the actions the agent can take.": "控制智能体可执行的操作权限。",
    "File Access Rules": "文件访问规则",
    "Configure allowed and denied paths for file reads and writes.": "配置允许和拒绝的文件读取与写入路径。",
    "Network Access Rules": "网络访问规则",
    "Configure allowed and denied URLs for reading.": "配置允许和拒绝抓取的网址列表。",
    "Terminal Commands": "终端命令权限",
    "Configure allowed terminal commands.": "配置允许执行的终端命令及模式。",
    "MCP Tools": "MCP 工具权限",
    "Configure external tools via Model Context Protocol.": "通过模型上下文协议 (Model Context Protocol) 配置外部工具。",
    "Folders": "关联文件夹",
    "Add Folder": "添加文件夹",
    "+ Add Folder": "+ 添加文件夹",
    "Open": "打开配置",
    "Edit": "编辑",
    "Delete": "删除",
    "Remove": "移除",

    // 权限预设下拉菜单各项
    "Inherit Global": "继承全局权限",
    "Inherits your Global Permissions when working in this project.": "在本项目中工作时，继承你的全局权限规则。",
    "Request Review": "请求人工审查",
    "Every command requires approval.": "每次执行命令与写入操作均需要人工审批。",
    "Default": "默认安全模式",
    "Ask before sensitive operations.": "在执行高危或敏感操作前请求人工确认。",
    "Turbo": "极速免审核模式 (Turbo)",
    "Run all commands without restrictions.": "无限制自动执行所有命令，高效全自动推进。",

    // 方案审查与行为
    "Agent Behavior": "智能体行为规范",
    "Plan Review Policy": "方案审查策略",
    "Whether the agent asks you to review its documents.": "智能体在生成规划与设计文档后是否请求审查。",
    "Always Proceed": "始终自动推进",
    "Ask Before Proceeding": "推进前请求确认",

    // 浏览器操作
    "Browser": "浏览器操作",
    "Browser Javascript Execution Policy": "浏览器 JS 执行策略",
    "Controls whether the agent can run custom JavaScript to automate complex browser actions.": "控制智能体是否可运行自定义 JavaScript 脚本以自动化复杂浏览器操作。",
    "Browser Actuation Rules": "浏览器交互驱动规则",
    "Configure allowed and denied URLs for browser actuation.": "配置允许和拒绝进行交互驱动的网址列表。",

    // 账户与方案
    "Enable Telemetry": "启用遥测数据收集",
    "When toggled on, Antigravity collects usage data to help Google enhance performance and features.": "开启后，Antigravity 将收集使用数据以帮助 Google 提升性能与改进功能。",
    "Marketing Emails": "营销与产品资讯邮件",
    "Receive product updates, tips, and promotions from Google Antigravity via email.": "通过电子邮件接收来自 Google Antigravity 的产品更新、技巧与促销活动。",
    "Your Plan:": "你的当前订阅方案：",
    "Google AI Pro": "Google AI 专业版 (Pro)",
    "You can upgrade to a Google AI Ultra plan to receive higher rate limits.": "你可以升级到 Google AI Ultra 方案以获得更高的请求频控限额。",
    "Upgrade": "升级方案",
    "Email": "电子邮箱",
    "Sign Out": "退出登录",
    "By using this app, you agree to its": "使用此应用即表示你同意其",
    "Terms of Service": "服务条款",

    // 外观与主题
    "Configure the agent's visual theme and display preferences.": "配置智能体的视觉主题与界面显示偏好。",
    "Theme": "界面主题",
    "Contrast": "对比度",
    "Strong": "高对比度",
    "Light Theme": "浅色主题配置",
    "Preset": "预设方案",
    "Default Light": "默认明亮",
    "Background": "背景色",
    "Foreground": "前景色",
    "Accent": "强调高亮色",
    "Chat Settings": "聊天界面设置",
    "Verbose Agent Chat": "详细输出模式",
    "Display and preserve intermediate thinking steps.": "完整展示并保留智能体的中间推理思考过程。",
    "Conversation Width": "会话面板宽度",
    "Configure the maximum width of the conversation panel.": "配置会话聊天面板的最大显示宽度。",
    "Narrow": "紧凑模式",
    "Wide": "宽屏模式",
    "Light": "明亮浅色",
    "Dark": "沉浸暗黑",
    "System": "跟随系统",

    // 应用程序设置
    "Manage Antigravity app settings.": "管理 Antigravity 桌面客户端的核心系统设置。",

    // 模型选择与用量配额
    "Model": "模型选择",
    "View Usage": "查看用量配额",
    "Leaving Soon": "即将下线",
    "Notice": "使用须知",
    "Review": "审查",
    "Low": "低",
    "Medium": "中",
    "High": "高",

    // 常用通用按钮
    "Accept": "接受变更",
    "Reject": "拒绝变更",
    "Accept All": "全部接受",
    "Reject All": "全部拒绝",
    "Proceed": "继续推进",
    "Cancel": "取消",
    "Send": "发送",
    "Stop": "停止",
    "Run": "运行",
    "Retry": "重试",
    "Copy": "复制",
    "Copied": "已复制",
    "Diff": "代码对比",
    "Submit": "提交",
    "Search": "搜索",
    "Close": "关闭",
    "Back": "返回",
    "Next": "下一步",
    "Finish": "完成",
    "Ask anything, @ to mention, / for actions": "输入你的需求，输入 @ 引用上下文，输入 / 快捷指令"
  };

  function translateTimeString(timeStr) {
    if (!timeStr) return timeStr;
    return timeStr
      .replace(/(\d+)\s*days?/gi, '$1 天')
      .replace(/(\d+)\s*hours?/gi, '$1 小时')
      .replace(/(\d+)\s*minutes?/gi, '$1 分钟')
      .replace(/(\d+)\s*seconds?/gi, '$1 秒')
      .replace(/,\s*/g, ' ');
  }

  function shouldPreserveAsIs(text, node) {
    if (!text) return true;
    const t = text.trim();
    if (USER_PROJECT_NAMES.has(t)) return true;
    if (t.endsWith('/') && t.length > 2) return true;

    // 检查 DOM 特征：若该文本前面有 SVG 文件夹图标，说明是项目或文件夹名称，绝不汉化！
    if (node && node.parentElement) {
      const parent = node.parentElement;
      const prev = parent.previousElementSibling || node.previousElementSibling;
      if (prev && prev.tagName && prev.tagName.toLowerCase() === 'svg') {
        return true;
      }
      if (parent.className && typeof parent.className === 'string' && parent.className.includes('text-muted-foreground')) {
        const grandParent = parent.parentElement;
        if (grandParent && grandParent.querySelector && grandParent.querySelector('svg')) {
          if (t === "Agent" || t === "agent") return true;
        }
      }
    }

    return false;
  }

  function translateStr(str, node) {
    if (!str) return null;
    const clean = str.replace(/\s+/g, ' ').trim();
    if (!clean || shouldPreserveAsIs(clean, node)) return null;

    if (STATIC_DICT[clean]) return STATIC_DICT[clean];

    // 1. 危险区域动态文案
    let m = clean.match(/^Permanently delete (.+?) including (\d+) active conversations\.?$/i);
    if (m) {
      const proj = m[1];
      const count = m[2];
      return `永久删除 ${proj}，包含 ${count} 个活跃对话。`;
    }

    // 2. 细分项统计: Show X breakdown(s)
    m = clean.match(/^Show (\d+) breakdowns?$/i);
    if (m) return `查看 ${m[1]} 项细分`;

    // 3. 动态正则匹配 "Modified in X projects"
    m = clean.match(/^Modified in (\d+) projects?$/i);
    if (m) return `已在 ${m[1]} 个项目中自定义`;

    // 4. 反馈邮箱: Send feedback as xxx
    m = clean.match(/^Send feedback as (.+)$/i);
    if (m) return `以 ${m[1]} 身份发送反馈`;

    // 5. 大模型时间限制动态匹配
    m = clean.match(/^You have used some of your weekly limit, it will fully refresh in (.+?)\.?$/i);
    if (m) return `你已消耗了部分每周限额，将在 ${translateTimeString(m[1])} 后完全重置。`;

    m = clean.match(/^You have used some of your 5-hour limit, it will fully refresh in (.+?)\.?$/i);
    if (m) return `你已消耗了部分 5 小时限额，将在 ${translateTimeString(m[1])} 后完全重置。`;

    m = clean.match(/^You have hit your weekly limit, it refreshes in (.+?)\.\s*If on a supported paid plan, you can use AI credits in the interim or upgrade to a higher tier\.?$/i);
    if (m) return `你的每周配额已耗尽，将在 ${translateTimeString(m[1])} 后重置。若使用支持的付费方案，期间可使用 AI 抵扣额度或升级到更高层级方案。`;

    m = clean.match(/^You have hit your weekly limit, the 5-hour limit does not currently apply\.\s*Your weekly limit will fully refresh in (.+?)\.?$/i);
    if (m) return `每周配额已耗尽，5 小时限额当前暂不适用。每周配额将在 ${translateTimeString(m[1])} 后完全重置。`;

    // 6. 前缀复合长句
    if (clean.startsWith("Controls the actions the agent can take.")) {
      const rest = clean.replace("Controls the actions the agent can take.", "").trim();
      const restTrans = translateStr(rest, node) || rest;
      return "控制智能体可执行的操作权限。 " + restTrans;
    }

    if (clean.startsWith("Whether the agent asks you to review its documents.")) {
      const rest = clean.replace("Whether the agent asks you to review its documents.", "").trim();
      const restTrans = translateStr(rest, node) || rest;
      return "智能体在生成规划与设计文档后是否请求审查。 " + restTrans;
    }

    // 7. 处理包含 "to be installed." 的复合句 (浏览器智能体)
    if (clean.includes("to be installed.") && clean.includes("在对话输入框输入")) {
      return clean.replace(/to be installed\./g, "。");
    }

    // 8. 处理单独含有 Project 的红色删除按钮
    if (clean === "Project" && node && node.parentElement) {
      const p = node.parentElement;
      if (p.textContent && (p.textContent.includes("删除") || p.className.includes("bg-destructive") || p.className.includes("text-destructive"))) {
        return "项目";
      }
    }

    // 9. 模型配额倒计时匹配: Resets in 1d / Resets in 3h 28m / Resets in 4h 59m
    let resetMatch = clean.match(/^Resets in (.*)$/i);
    if (resetMatch) {
      let t = resetMatch[1].trim();
      t = t.replace(/(\d+)\s*d/gi, '$1 天 ')
           .replace(/(\d+)\s*h/gi, '$1 小时 ')
           .replace(/(\d+)\s*m/gi, '$1 分钟 ')
           .replace(/(\d+)\s*s/gi, '$1 秒 ')
           .replace(/,/g, '')
           .trim();
      return `${t} 后重置`;
    }

    // 10. 会话简要说明长句与常见英文前缀动态汉化 (专有名词保留)
    if (clean.startsWith("This is a conversation about resolving an issue with \"waiting for Gateway connection\" in the context of the Openclaw project")) {
      return "解决 Openclaw 项目中“等待网关连接”故障";
    }
    if (clean.startsWith("This is a conversation about")) {
      let subject = clean.replace("This is a conversation about", "").trim();
      return "关于 " + subject + " 的会话";
    }
    let mTitle = clean.match(/^Install And (?:Open|Run) (.+)$/i);
    if (mTitle) return `安装并启动 ${mTitle[1]}`;
    mTitle = clean.match(/^Install (.+?) Tools?$/i);
    if (mTitle) return `安装 ${mTitle[1]} 工具`;
    mTitle = clean.match(/^Install (.+)$/i);
    if (mTitle) return `安装 ${mTitle[1]}`;
    mTitle = clean.match(/^Troubleshooting (.+)$/i);
    if (mTitle) return `排查 ${mTitle[1]} 问题`;
    mTitle = clean.match(/^Optimizing (.+)$/i);
    if (mTitle) return `优化 ${mTitle[1]}`;
    mTitle = clean.match(/^Building (.+)$/i);
    if (mTitle) return `构建 ${mTitle[1]}`;

    if (clean === "View Usage" || clean.startsWith("View Usage")) {
      return "查看用量配额";
    }
    let mSeeAll = clean.match(/^See all \((\d+)\)$/i);
    if (mSeeAll) return `查看全部 (${mSeeAll[1]})`;
    if (clean === "See all") return "查看全部";

    return null;
  }

  // 恢复被误翻为“智能体”的项目文件夹名称为“Agent”
  function restoreMistranslatedProjectNodes() {
    const all = document.querySelectorAll('*');
    for (const el of all) {
      if (el.children.length === 0 && el.textContent.trim() === "智能体") {
        const parent = el.parentElement;
        if (!parent) continue;
        const prev = el.previousElementSibling || parent.previousElementSibling;
        const hasSvg = (prev && prev.tagName && prev.tagName.toLowerCase() === 'svg') ||
                        (parent.querySelector && parent.querySelector('svg')) ||
                        (parent.className && typeof parent.className === 'string' && (parent.className.includes('truncate') || parent.className.includes('text-sm') || parent.className.includes('select-none')));
        
        if (hasSvg || el.closest?.('[data-testid*="project"]') || el.className?.includes('truncate')) {
          if (el.firstChild) {
            el.firstChild.nodeValue = "Agent";
          } else {
            el.textContent = "Agent";
          }
        }
      }
    }
  }

  // 专用增强：针对复合内联元素（如 Danger Zone 红色按钮、包含 kbd 的说明等）直接做 DOM 修正
  function fixSpecialDOMElements() {
    // 1. 修复红色删除项目按钮：如果文本是 "删除Project" 或 "Delete Project"
    document.querySelectorAll('button').forEach(btn => {
      const txt = btn.textContent.trim();
      if (txt === "删除Project" || txt === "Delete Project" || txt === "DeleteProject") {
        btn.textContent = "删除项目";
      }
    });

    // 2. 深度修复 plan 方案审查说明条 (解决深层嵌套 TextNode 问题)
    document.querySelectorAll('*').forEach(el => {
      if (el.textContent && el.textContent.includes('generate a plan') && el.textContent.includes('Type')) {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while (n = walker.nextNode()) {
          const v = n.nodeValue.trim();
          if (v === "Type") {
            n.nodeValue = "输入 ";
          } else if (v === "and select") {
            n.nodeValue = " 并选择 ";
          } else if (v === "to have the agent generate a plan." || v === "to have the agent generate a plan") {
            n.nodeValue = " 让智能体生成执行方案。";
          }
        }
      }
    });

    // 3. 深度修复 Also includes ... when working in this project (被 a 标签切断的整句)
    document.querySelectorAll('*').forEach(el => {
      if (el.textContent && el.textContent.includes('working in this project') && (el.textContent.includes('Also includes') || el.textContent.includes('同时包含') || el.textContent.includes('在本项目中'))) {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while (n = walker.nextNode()) {
          const v = n.nodeValue.trim();
          if (v === "Also includes") {
            n.nodeValue = "在本项目中工作时，亦包含 ";
          } else if (v.startsWith("when working in this project")) {
            n.nodeValue = n.nodeValue.replace(/when working in this project\.?/i, "（在本项目中生效）。");
          }
        }
      }
    });

    // 4. 深度修复 active conversations (危险区域动态对话数量)
    document.querySelectorAll('*').forEach(el => {
      if (el.textContent && /active conversations/i.test(el.textContent)) {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while (n = walker.nextNode()) {
          if (/active conversations/i.test(n.nodeValue)) {
            n.nodeValue = n.nodeValue
              .replace(/(\d+)\s*active conversations\.?/gi, '$1 个活跃对话。')
              .replace(/active conversations\.?/gi, '个活跃对话。');
          }
        }
      }
    });

    // 5. 修复未归属项目会话副标题 (outside of projects)
    document.querySelectorAll('*').forEach(el => {
      if (el.textContent && el.textContent.includes('outside of projects')) {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while (n = walker.nextNode()) {
          if (n.nodeValue.includes('Agent settings and permissions for conversations outside of projects')) {
            n.nodeValue = "配置未归属项目的会话智能体设定及权限规则。";
          }
        }
      }
    });

    // 6. 修复浏览器子智能体文案容器
    document.querySelectorAll('div, p, span').forEach(el => {
      if (el.children.length > 0 && el.querySelector('a')) {
        const full = el.textContent.replace(/\s+/g, ' ').trim();
        if (full.includes("Configure the browser subagent") || (full.includes("Google Chrome") && full.includes("browser"))) {
          Array.from(el.childNodes).forEach(child => {
            if (child.nodeType === Node.TEXT_NODE) {
              const val = child.nodeValue.trim();
              if (val.startsWith("Configure the browser subagent. It requires")) {
                child.nodeValue = "配置浏览器子智能体。此功能需要已安装 ";
              } else if (val.startsWith("to be installed.")) {
                child.nodeValue = val.replace("to be installed.", "。");
              }
            }
          });
        }
    // 7. 强化 View Usage 菜单项
    document.querySelectorAll('*').forEach(el => {
      if (el.textContent && el.textContent.includes('View Usage')) {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while (n = walker.nextNode()) {
          if (n.nodeValue.trim() === 'View Usage') {
            n.nodeValue = '查看用量配额';
          }
        }
      }
    });

    // 8. 强化 See all (X)
    document.querySelectorAll('*').forEach(el => {
      if (el.textContent && /See all/i.test(el.textContent)) {
        const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        let n;
        while (n = walker.nextNode()) {
          const m = n.nodeValue.trim().match(/^See all\s*\((.+?)\)$/i);
          if (m) {
            n.nodeValue = `查看全部 (${m[1]})`;
          } else if (n.nodeValue.trim() === 'See all') {
            n.nodeValue = '查看全部';
          }
        }
      }
    });
  }

  function processNode(node) {
    if (!node) return;

    if (node.nodeType === Node.ELEMENT_NODE) {
      const tag = node.tagName.toLowerCase();
      if (['script', 'style', 'code', 'pre', 'textarea'].includes(tag)) return;
      if (node.isContentEditable) return;

      for (const attr of ['placeholder', 'title', 'aria-label', 'tooltip']) {
        const val = node.getAttribute(attr);
        if (val) {
          const trans = translateStr(val, node);
          if (trans && trans !== val) node.setAttribute(attr, trans);
        }
      }
    }

    if (node.nodeType === Node.TEXT_NODE) {
      const p = node.parentElement;
      if (p) {
        const pTag = p.tagName.toLowerCase();
        if (['code', 'pre', 'script', 'style', 'textarea'].includes(pTag)) {
          return;
        }
        if (p.isContentEditable) return;
      }

      const val = node.nodeValue;
      if (val && val.trim()) {
        const trans = translateStr(val, node);
        if (trans && trans !== val) {
          node.nodeValue = trans;
        }
      }
      return;
    }

    let child = node.firstChild;
    while (child) {
      processNode(child);
      child = child.nextSibling;
    }
  }

  function sweep() {
    processNode(document.body);
    const popovers = document.querySelectorAll('[role="dialog"], [role="listbox"], [role="menu"], [role="tooltip"], [data-radix-popper-content-wrapper], [data-radix-menu-content], div.fixed.inset-0');
    popovers.forEach(el => processNode(el));
    fixSpecialDOMElements();
    restoreMistranslatedProjectNodes();
  }

  sweep();

  const obs = new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.type === 'childList') {
        m.addedNodes.forEach(n => processNode(n));
      } else if (m.type === 'characterData') {
        const val = m.target.nodeValue;
        if (val && val.trim()) {
          const trans = translateStr(val, m.target);
          if (trans && trans !== val) {
            m.target.nodeValue = trans;
          }
        }
      }
    }
    fixSpecialDOMElements();
    restoreMistranslatedProjectNodes();
  });

  obs.observe(document.body, { childList: true, subtree: true, characterData: true });
  window.__ANTIGRAVITY_ZH_OBSERVER__ = obs;

  window.__ANTIGRAVITY_ZH_INTERVAL__ = setInterval(sweep, 250);

  console.log('[Antigravity-ZH] 🚀 全界面终极高精汉化补丁已加载！');
})();
