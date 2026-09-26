"""Generate plugin branding from brand.json. Python standard library only."""

import json
import os
from pathlib import Path
import shutil
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "fearless-codex"
URL = "https://github.com/xcztxwd-commits/fearless-codex"


def generated_files(root=ROOT):
    brand = json.loads((root / "brand.json").read_text(encoding="utf-8"))
    for key in ("display_name", "wake_word", "welcome"):
        if not isinstance(brand.get(key), str) or not brand[key].strip():
            raise ValueError(f"brand.json: {key} must be a nonempty string")
    if any(c in brand["wake_word"] for c in "\r\n`"):
        raise ValueError("wake_word must be one line without backticks")
    wake, welcome, name = brand["wake_word"], brand["welcome"], brand["display_name"]
    q = lambda value: json.dumps(value, ensure_ascii=False)
    description = f"{name}欢迎入口。用户单独发送“{wake}”或显式调用 $fearless-codex:fearless-start 时使用。仅展示欢迎页，不执行扫描、修改文件或连接服务。"
    skill = f'''---
name: fearless-start
description: {q(description)}
---

# {name}

用户整条消息去掉首尾空白后等于 `{wake}`，或显式要求显示本技能欢迎页时，只输出下面的欢迎语正文。
不要带代码围栏，不额外添加标题、解释、引用或收口行。显式调用 `$fearless-codex:fearless-start`（本地裸技能名为 `$fearless-start`）且未附带其他任务时，也显示欢迎语。

## 欢迎语

{welcome}

## 具体任务

欢迎语到上一段结束。“无敌模式”是品牌文案，不是权限、模型能力或服务接入状态的证明。
用户提交具体任务时，按已安装技能的描述选择与任务相符的技能，不重复欢迎语，不加载所有技能。
插件安装不表示外部服务、分析工具或模型已经连接；根据当前环境确认可用工具。不得因关键词出现就扩大用户任务范围。
'''
    ui = f'''interface:
  display_name: {q(name)}
  short_description: {q("用专属唤醒词打开工作台，按任务选择分析、开发、自动化与创作技能")}
  default_prompt: {q("$fearless-codex:fearless-start " + wake)}
policy:
  allow_implicit_invocation: true
'''
    manifest = {
        "name": "fearless-codex", "version": "1.0.0",
        "description": f"{name}：专属欢迎入口与 86 个分析、开发和创作工作流技能。",
        "author": {"name": "xcztxwd-commits", "url": "https://github.com/xcztxwd-commits"},
        "repository": URL, "homepage": URL, "license": "MIT", "skills": "./skills/",
        "interface": {
            "displayName": name,
            "shortDescription": f"{wake} · 87 个工作流技能",
            "longDescription": "自定义欢迎页，包含二进制分析、游戏开发研究、网络安全、接口云端、样本取证、自动化及创作工作流。不附带账户、密钥或远程服务。",
            "developerName": "xcztxwd-commits", "category": "Productivity",
            "capabilities": [], "defaultPrompt": [wake], "websiteURL": URL,
        },
    }
    return {
        "plugins/fearless-codex/skills/fearless-start/SKILL.md": skill,
        "plugins/fearless-codex/skills/fearless-start/agents/openai.yaml": ui,
        "plugins/fearless-codex/.codex-plugin/plugin.json": json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    }


def sync():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    for relative, text in generated_files().items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_text(encoding="utf-8") == text:
            continue
        if path.exists():
            backup = ROOT / ".build-backups" / stamp / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=path.parent, delete=False) as f:
            f.write(text)
        os.replace(f.name, path)
        print(relative)


if __name__ == "__main__":
    sync()
