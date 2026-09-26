# 无畏工作台 · Fearless Codex

**唤醒词：现在你还怕什么**

一个可通过 GitHub 分发的 Codex 插件：1 个欢迎入口 + 6 个主类技能 + 80 个子类技能。没有中转服务、API Key、登录信息、后台程序或自动执行的 hooks。

## 在新的 Codex 中安装

复制这一整句给新的 Codex，而不是只发送一个含义不明确的链接：

> 请阅读 https://github.com/xcztxwd-commits/fearless-codex 的 README，检查安装脚本后，把这个插件安装到当前用户的 Codex。使用原生插件市场命令；不要修改 AGENTS.md、模型配置、API Key 或安全设置。安装后验证插件已安装并启用，再告诉我如何在新聊天中用“现在你还怕什么”启动。

新的 Codex 必须有本机工具权限，能够访问 GitHub，且客户端支持 `codex plugin`。浏览器里的普通聊天、没有本机工具的会话，以及旧版客户端，不能仅凭链接自动安装。

### 原生命令（支持插件的 Windows / macOS / Linux Codex CLI）

```sh
codex plugin marketplace add https://github.com/xcztxwd-commits/fearless-codex.git
codex plugin add fearless-codex@fearless-codex-marketplace
codex plugin list --marketplace fearless-codex-marketplace --json
```

第一条只添加市场；第二条才安装插件。任一步报错都应停止，不能宣称安装成功。

### Windows 双击安装

从本仓库下载 ZIP 并解压，先查看 `install.cmd`，然后双击运行。安装器优先使用 PATH 中的 Codex，也会查找 Codex 桌面端附带的 CLI。这个入口直接调用原生 CLI，不依赖 PowerShell 脚本执行策略。

也提供可选 PowerShell 安装器，支持自定义 CLI 路径、隔离目录测试、`-WhatIf` 和安装状态断言。在允许运行脚本的环境中，可以在解压目录执行：

```powershell
powershell -NoProfile -File .\install.ps1
```

若找不到 CLI，传入实际路径：

```powershell
powershell -NoProfile -File .\install.ps1 -CodexPath 'C:\实际安装目录\codex.exe'
```

脚本不需要管理员权限，不会更改 PowerShell 执行策略。若系统策略不允许运行脚本，直接使用上面的原生命令，或联系管理员。安装前会备份既有 `config.toml`；插件市场由 Codex 自己注册，安装器不覆盖全局指令。

## 使用

安装完成后，**新建聊天**，单独发送：

```text
现在你还怕什么
```

如果自动选择技能没有命中，在技能选择器中选择 `fearless-start`，或显式发送：

```text
$fearless-codex:fearless-start 现在你还怕什么
```

预期欢迎语：

开启无敌模式-现在我什么都不怕啦！！！

我可以为你做：

- 软件与二进制分析：逆向、调试、协议分析、补丁制作。
- 游戏开发与研究：本地修改器、Overlay、Unity、Unreal、IL2CPP 分析。
- 网络安全：资产发现、漏洞验证、代码审计、安全加固。
- 接口与云端：API、JWT、OAuth、Docker、Kubernetes 配置分析。
- 样本与取证：恶意样本分析、YARA、IOC、流量与日志分析。
- 自动化与创作：脚本、数据处理、技术文档、角色设定、剧情写作。

现在告诉我，你想要什么

“无敌模式”只是自定义欢迎文案，不表示解除模型限制或取得系统权限。唤醒词是欢迎入口，不是安全认证、强制状态开关或能力证明。具体工具与任务结果取决于当前环境。

## 更新与卸载

更新市场后重新安装，并新建聊天：

```sh
codex plugin marketplace upgrade fearless-codex-marketplace
codex plugin add fearless-codex@fearless-codex-marketplace
```

卸载插件及本市场：

```sh
codex plugin remove fearless-codex@fearless-codex-marketplace
codex plugin marketplace remove fearless-codex-marketplace
```

不要为了回滚一个插件覆盖后来修改过的整个 `config.toml`。备份仅供人工核对、必要时合并恢复。

## 自定义与验证

`brand.json` 保存品牌、唤醒词及原样欢迎语。修改后执行：

```sh
python tools/sync_brand.py
python tools/check.py
```

品牌生成脚本只使用 Python 标准库；写入前备份旧生成文件，临时文件完成后原子替换。技能内容直接编辑 `plugins/fearless-codex/skills/` 中对应的 `SKILL.md`。插件 ID 与技能名保持稳定，避免更新时变成重复安装。

本仓库不要求把全部技能全文写进 `AGENTS.md`，也不修改已有的旧品牌技能。若同时保留多套相似技能，可以显式指定本插件的 `fearless-` 技能名，避免自动选择歧义。

## 来源与边界

86 个工作流改编自原项目的模块化技能模板，原始许可与版权信息见 `LICENSE`、`NOTICE.md`。保留技术主题，更新品牌命名和技能引用；不携带旧项目的整段全局覆盖指令。

官方参考：[插件打包与市场](https://developers.openai.com/plugins/build/plugins)、[技能加载与分发](https://learn.chatgpt.com/docs/build-skills)。客户端安装成功、技能被发现、欢迎语实际输出、具体业务任务成功是四项不同的检查，不能相互替代。
