#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Antigravity 简体中文编程词典与规范生成器
提供精准的技术词汇中英对照、规范的中文注释与提交模板
"""

from typing import Dict, List, Optional

# 高频编程与架构术语中英精准对照表（避免生硬机翻）
TECH_DICTIONARY: Dict[str, Dict[str, str]] = {
    "pipeline": {
        "zh": "流水线 / 处理管线",
        "example": "数据清洗流水线 (Data Cleaning Pipeline)"
    },
    "ingestion": {
        "zh": "数据摄取 / 数据采集",
        "example": "日志摄取服务 (Log Ingestion Service)"
    },
    "enrichment": {
        "zh": "数据富化 / 数据增强",
        "example": "线索富化引擎 (Lead Enrichment Engine)"
    },
    "deduplication": {
        "zh": "去重 / 实体查重",
        "example": "基于向量的实体查重 (Vector-based Deduplication)"
    },
    "middleware": {
        "zh": "中间件",
        "example": "身份认证中间件 (Auth Middleware)"
    },
    "payload": {
        "zh": "负载 / 请求载荷",
        "example": "Webhook 请求载荷 (Webhook Payload)"
    },
    "idempotent": {
        "zh": "幂等的",
        "example": "保证支付回调操作幂等 (Ensure Idempotent Operation)"
    },
    "concurrency": {
        "zh": "并发控制",
        "example": "最大并发请求数 (Max Concurrency)"
    },
    "rate limiting": {
        "zh": "速率限制 / 频控",
        "example": "API 频控策略 (API Rate Limiting)"
    },
    "fallback": {
        "zh": "降级方案 / 兜底策略",
        "example": "大模型调用超时降级策略 (Model Fallback Strategy)"
    },
    "retry with backoff": {
        "zh": "指数退避重试",
        "example": "网络异常指数退避重试 (Exponential Backoff Retry)"
    },
    "schema": {
        "zh": "结构模式 / 数据约束模式",
        "example": "Pydantic 数据模式 (Pydantic Schema)"
    },
    "refactor": {
        "zh": "代码重构",
        "example": "模块化重构 (Modular Refactoring)"
    },
    "circuit breaker": {
        "zh": "熔断器",
        "example": "第三方接口熔断保护 (Circuit Breaker)"
    },
    "state machine": {
        "zh": "状态机",
        "example": "工单状态流转状态机 (Workflow State Machine)"
    },
    "debounce": {
        "zh": "防抖",
        "example": "搜索输入防抖 (Search Input Debounce)"
    },
    "throttle": {
        "zh": "节流",
        "example": "滚动事件节流 (Scroll Throttle)"
    },
    "dry run": {
        "zh": "空跑演练 / 试运行",
        "example": "上线前空跑演练 (Pre-release Dry Run)"
    }
}

# 遵循 Conventional Commits 的中文提交前缀
COMMIT_TYPES = {
    "feat": "✨ 新增功能 (feat)",
    "fix": "🐛 修复缺陷 (fix)",
    "docs": "📝 文档更新 (docs)",
    "style": "💄 代码样式调整 (style, 不影响逻辑)",
    "refactor": "♻️ 代码重构 (refactor, 既非新增也非修 bug)",
    "perf": "⚡️ 性能优化 (perf)",
    "test": "✅ 测试用例 (test)",
    "chore": "🔧 构建或辅助工具变动 (chore)",
    "revert": "⏪️ 代码回退 (revert)"
}

class ChineseProgrammingHelper:
    """中文编程辅助工具类"""

    @staticmethod
    def lookup_term(query: str) -> List[Dict[str, str]]:
        """在术语库中搜索技术词汇"""
        q = query.strip().lower()
        results = []
        for en, item in TECH_DICTIONARY.items():
            if q in en.lower() or q in item["zh"]:
                results.append({
                    "term": en,
                    "zh": item["zh"],
                    "example": item["example"]
                })
        return results

    @staticmethod
    def get_commit_types() -> Dict[str, str]:
        """获取中文规范的 Commit 类型列表"""
        return COMMIT_TYPES

    @staticmethod
    def generate_jsdoc_template(func_name: str, params: List[str], return_type: str = "Promise<any>") -> str:
        """生成符合中文规范的 TypeScript/JSDoc 注释模板"""
        lines = [
            "/**",
            f" * 业务功能：[请简述 {func_name} 的核心职责]",
            " *"
        ]
        for p in params:
            lines.append(f" * @param {p} [参数说明与校验约束]")
        lines.append(f" * @returns {{{return_type}}} [返回值含义说明]")
        lines.append(" * @throws {Error} [可能抛出的业务或系统异常]")
        lines.append(" */")
        return "\n".join(lines)

    @staticmethod
    def generate_python_docstring(func_name: str, args: List[str], return_type: str = "dict") -> str:
        """生成符合 Google 规范的中文 Python Docstring 模板"""
        lines = [
            f'"""{func_name} 业务功能描述。',
            '',
            '详细设计与逻辑说明：',
            '    1. 执行前置参数校验',
            '    2. 核心业务计算或数据处理',
            '    3. 异常捕获与兜底返回',
            '',
            'Args:'
        ]
        for a in args:
            lines.append(f'    {a}: 参数含义、类型及取值范围。')
        lines.extend([
            '',
            'Returns:',
            f'    {return_type}: 处理完成后的返回结果说明。',
            '',
            'Raises:',
            '    ValueError: 参数不合法时抛出。',
            '    Exception: 外部 API 或系统调用失败时抛出。',
            '"""'
        ])
        return "\n".join(lines)
